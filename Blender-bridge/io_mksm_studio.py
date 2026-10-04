bl_info = {'name': 'MKSM Studio Bridge', 'author': 'OG Midway', 'version': (0, 26, 0), 'blender': (4, 2, 0), 'location': '3D View > Sidebar > MKSM', 'description': 'Import original MKSM rigs and export shape edits or replacement meshes for MKSM Studio', 'category': 'Import-Export'}
import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, PointerProperty, CollectionProperty
import os
import json
import subprocess
import tempfile
import textwrap
from pathlib import Path

class MKSM_OT_import(bpy.types.Operator, ImportHelper):
    bl_idname = 'mksm.import_model'
    bl_label = 'Open original MKSM model (.glb)'
    filename_ext = '.glb'
    filter_glob: StringProperty(default='*.glb', options={'HIDDEN'})
    def execute(self, context):
        manifest_path=Path(self.filepath).parent/'animation-manifest.json'
        manifest=json.loads(manifest_path.read_text(encoding='utf-8-sig')) if manifest_path.is_file() else None
        if manifest:
            fps=manifest.get('PreviewFramesPerSecond',30)
            context.scene.render.fps=int(round(fps));context.scene.render.fps_base=context.scene.render.fps/fps
        bpy.ops.import_scene.gltf(filepath=self.filepath, merge_vertices=False)
        if manifest:
            context.scene.mksm_animation_manifest=str(manifest_path)
            if len(manifest.get('Clips',[]))==1:
                clip=manifest['Clips'][0];context.scene.frame_start=0;context.scene.frame_end=clip['DurationFrames']-1
                for rig in context.selected_objects:
                    if rig.type!='ARMATURE' or not rig.animation_data:continue
                    ad=rig.animation_data
                    actions=[strip.action for track in ad.nla_tracks for strip in track.strips if strip.action.name.startswith(clip['Name'])]
                    if len(actions)==1:
                        for track in ad.nla_tracks:track.mute=True
                        ad.action=actions[0]
        game_rigs = [o for o in context.selected_objects if o.type=='ARMATURE' and o.get('mksm_source_sha256')]
        if len(game_rigs)==1:context.scene.mksm_target_rig=game_rigs[0]
        snapshot = str(Path(self.filepath).with_suffix('.original.pme2'))
        if Path(snapshot).is_file():
            context.scene.mksm_native_source = snapshot
            context.scene.mksm_template_glb = self.filepath
        return {'FINISHED'}

class MKSM_OT_export(bpy.types.Operator, ExportHelper):
    bl_idname = 'mksm.export_edits'
    bl_label = 'Save shape / UV edits (.glb)'
    filename_ext = '.glb'
    filter_glob: StringProperty(default='*.glb', options={'HIDDEN'})
    def execute(self, context):
        if context.object and context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Switch to Object Mode before exporting.')
            return {'CANCELLED'}
        meshes = [o for o in context.scene.objects if o.type == 'MESH' and ('mksm_chunk' in o or o.get('mksm_grouped') == 1)]
        if not meshes:
            self.report({'ERROR'}, 'Open a GLB exported by MKSM Studio first.')
            return {'CANCELLED'}
        if len({o.get('mksm_source_sha256') for o in meshes}) != 1:
            self.report({'ERROR'}, 'Use one original MKSM model per scene when exporting edits.')
            return {'CANCELLED'}
        if any('_MKSM_VERTEX' not in o.data.attributes or (o.get('mksm_grouped') == 1 and '_MKSM_PART' not in o.data.attributes) for o in meshes):
            self.report({'ERROR'}, 'Native vertex IDs are missing. Start from a fresh Studio export.')
            return {'CANCELLED'}
        if any(m.type != 'ARMATURE' and m.show_viewport for o in meshes for m in o.modifiers):
            self.report({'ERROR'}, 'Shape import preserves topology. Remove unapplied mesh modifiers before exporting.')
            return {'CANCELLED'}
        rigs = {m.object for o in meshes for m in o.modifiers if m.type == 'ARMATURE' and m.object}
        selected = list(context.selected_objects); active = context.view_layer.objects.active
        objects = meshes + list(rigs)
        hidden = {o:(o.hide_get(),o.hide_viewport,o.hide_select) for o in objects}
        try:
            bpy.ops.object.select_all(action='DESELECT')
            for o in objects:
                o.hide_viewport=False; o.hide_set(False); o.hide_select=False; o.select_set(True)
            result=bpy.ops.export_scene.gltf(filepath=self.filepath, export_format='GLB', use_selection=True, export_attributes=True, export_extras=True, export_skins=True, export_animations=False, export_apply=False, export_def_bones=False, export_rest_position_armature=True, export_yup=True)
        finally:
            bpy.ops.object.select_all(action='DESELECT')
            for o,(local,view,select) in hidden.items():
                o.hide_set(local); o.hide_viewport=view; o.hide_select=select
            for o in selected:o.select_set(True)
            context.view_layer.objects.active=active
        self.report({'INFO'}, 'Open this GLB with Import Blender edits in Studio. Native skeleton, weights and topology are preserved.')
        return result

def _mksm_weight_plan(obj, rig, max_loss):
    import itertools
    import heapq
    import math
    names = set(rig.data.bones.keys())
    original = []
    for vertex in obj.data.vertices:
        weights = {obj.vertex_groups[g.group].name: float(g.weight) for g in vertex.groups
                   if g.weight > 0 and obj.vertex_groups[g.group].name in names}
        if not weights or any(not math.isfinite(w) for w in weights.values()):
            raise ValueError(f'{obj.name}: vertex {vertex.index} has missing/invalid bone weights. Cleanup cannot invent weights.')
        total = sum(weights.values()); original.append({k: v / total for k, v in weights.items()})
    def quantize(row):
        total = sum(row.values()); exact = {k: v / total * 4096 for k, v in row.items()}
        fixed = {k: math.floor(v) for k, v in exact.items()}
        for k in sorted(exact, key=lambda k: (-(exact[k] - fixed[k]), k))[:4096 - sum(fixed.values())]: fixed[k] += 1
        return {k: v / 4096 for k, v in fixed.items() if v}
    def loss(index, palette): return max(0, 1 - sum(v for k, v in original[index].items() if k in palette))
    weights = [quantize(row) for row in original]
    # A compatible triangle cannot include a vertex with more than three bones.
    # Keep its strongest three, then solve the shared palette across corners.
    for i, row in enumerate(weights):
        if len(row) > 3:
            weights[i] = quantize(dict(sorted(row.items(), key=lambda kv: (-kv[1], kv[0]))[:3]))
        if loss(i, weights[i]) > max_loss + 1e-8:
            raise ValueError(f'{obj.name}: vertex {i} needs {loss(i, weights[i]):.1%} removed, above the {max_loss:.0%} limit. Raise Max weight removed only after reviewing, or adjust those weights manually. Original untouched.')
    obj.data.calc_loop_triangles(); triangles = [tuple(t.vertices) for t in obj.data.loop_triangles]
    adjacency = [[] for _ in weights]
    for i, tri in enumerate(triangles):
        for v in tri: adjacency[v].append(i)
    def palette(tri): return set().union(*(weights[v] for v in tri))
    initial_bad = sum(len(set().union(*(original[v] for v in tri))) > 3 for tri in triangles)
    heap = []; revisions = [0] * len(triangles)
    def queue(i):
        revisions[i] += 1; tri = triangles[i]; union = palette(tri)
        if len(union) <= 3: return
        best = None; required = 1.0
        for candidate in itertools.combinations(sorted(union), 3):
            kept = [sum(w for k, w in weights[v].items() if k in candidate) for v in tri]
            if min(kept) <= 0: continue
            # Candidates cannot restore an influence removed by an earlier face.
            cumulative = [loss(v, set(candidate).intersection(weights[v])) for v in tri]
            required = min(required, max(cumulative))
            if max(cumulative) > max_loss + 1e-8: continue
            # Prefer smaller worst-vertex changes; deterministic ties make exports
            # reproducible. This is a local heuristic, not a global optimum.
            score = (max(cumulative), sum(1 - k for k in kept), candidate)
            if best is None or score < best: best = score
        if best is None:
            raise ValueError(f'{obj.name}: triangle {i + 1} needs at least {required:.1%} removed at a corner, above the {max_loss:.0%} limit. No original weights changed. Try a higher Max weight removed value on a preview copy, or edit that area manually.')
        # Resolve the tightest palettes first to reduce cascading removals.
        heapq.heappush(heap, (-best[0], best[1], i, revisions[i], best[2]))
    for i in range(len(triangles)): queue(i)
    while heap:
        _, _, i, revision, allowed = heapq.heappop(heap)
        if revision != revisions[i]: continue
        changed = []
        for v in triangles[i]:
            row = quantize({k: w for k, w in weights[v].items() if k in allowed})
            if row != weights[v]: weights[v] = row; changed.append(v)
        # Only remove influences: no neighboring triangle can gain a bone.
        for neighbor in sorted({n for v in changed for n in adjacency[v]}): queue(neighbor)
    if any(len(palette(tri)) > 3 for tri in triangles): raise RuntimeError('Cleanup validation failed; original weights untouched.')
    changes = []
    for i, (before, after) in enumerate(zip(original, weights)):
        removed = loss(i, after)
        if removed > max_loss + 1e-8: raise ValueError(f'{obj.name}: native weight rounding exceeds the chosen cleanup limit at vertex {i}.')
        if before != after:
            changes.append({'Vertex': i, 'Before': before, 'After': after, 'RemovedOriginalFraction': removed})
    return weights, {'Mesh': obj.name, 'Vertices': len(weights), 'TrianglesBeforeCleanup': len(triangles), 'IncompatibleTrianglesBefore': initial_bad,
                     'IncompatibleTrianglesAfter': 0, 'VerticesWithRemovedInfluences': sum(set(original[i]) != set(weights[i]) for i in range(len(weights))),
                     'VerticesAdjustedIncludingRounding': len(changes), 'MaximumRemovedFraction': max((r['RemovedOriginalFraction'] for r in changes), default=0), 'Changes': changes}


def _mksm_cleanup_copies(context, originals, rig):
    import bmesh
    # All mutation is confined to newly allocated meshes. The same function is
    # used for retained preview copies and temporary export copies.
    collection = bpy.data.collections.new('MKSM Weight Cleanup'); context.scene.collection.children.link(collection)
    copies = []; rows = []
    try:
        for source in originals:
            if source.data.shape_keys or any(m.type != 'ARMATURE' and (m.show_viewport or m.show_render) for m in source.modifiers):
                raise ValueError(f'{source.name}: apply Decimate/other mesh modifiers first. Keep the Armature modifier. Cleanup works on the resulting mesh.')
            arms = [m for m in source.modifiers if m.type == 'ARMATURE']
            if len(arms) != 1 or arms[0].object != rig: raise ValueError(f'{source.name}: use one Armature modifier pointing to the original rig.')
            obj = source.copy(); obj.data = source.data.copy(); copies.append(obj); collection.objects.link(obj)
            if 'mksm_prepared_id' in obj: del obj['mksm_prepared_id']
            obj.name = source.name + '_CleanWeights'; obj.hide_viewport = False; obj.hide_select = False; obj.hide_render = False; obj.hide_set(False)
            # Make the tested triangles explicit; GLB export cannot choose a
            # different diagonal through a quad/ngon and reintroduce four bones.
            if any(len(p.vertices) != 3 for p in obj.data.polygons):
                mesh = bmesh.new()
                try:
                    mesh.from_mesh(obj.data); bmesh.ops.triangulate(mesh, faces=list(mesh.faces), quad_method='BEAUTY', ngon_method='BEAUTY'); mesh.to_mesh(obj.data)
                finally: mesh.free()
            weights, report = _mksm_weight_plan(obj, rig, context.scene.mksm_cleanup_max_loss / 100)
            indices = {g.name: g for g in obj.vertex_groups if g.name in rig.data.bones}
            for group in indices.values(): group.remove(list(range(len(obj.data.vertices))))
            for vertex, row in enumerate(weights):
                for name, value in row.items(): indices[name].add([vertex], value, 'REPLACE')
            # Verify Blender's stored weights, not just the planned values.
            actual = [{obj.vertex_groups[g.group].name for g in v.groups if g.weight > 0 and obj.vertex_groups[g.group].name in indices} for v in obj.data.vertices]
            obj.data.calc_loop_triangles()
            if any(len(set().union(*(actual[v] for v in t.vertices))) > 3 for t in obj.data.loop_triangles): raise RuntimeError('Stored cleanup weights failed validation.')
            report['SourceMesh'] = source.name; rows.append(report)
        return copies, collection, {'Status': 'Cleaned export weights; preview movement before using in game', 'GameplayTested': False,
                                   'MaxAllowedRemovedFraction': context.scene.mksm_cleanup_max_loss / 100, 'Meshes': rows,
                                   'Method': 'Keep strongest influences; choose three-bone triangle palettes with the least local loss within the selected limit. Normalize to 1/4096. No new bone influences are added.',
                                   'Preserved': 'Original objects, weights, materials, UVs and skeleton. Copies keep vertex positions and materials; quads/ngons are triangulated.'}
    except Exception:
        _mksm_remove_cleanup(copies, collection); raise


def _mksm_remove_cleanup(objects, collection):
    for obj in objects:
        mesh = obj.data; bpy.data.objects.remove(obj, do_unlink=True)
        if mesh.users == 0: bpy.data.meshes.remove(mesh)
    if collection: bpy.data.collections.remove(collection)


def _mksm_save_cleanup_report(context, report):
    block = bpy.data.texts.new('MKSM Weight Cleanup Report'); block.write(json.dumps(report, indent=2))
    context.scene.mksm_cleanup_report = block.name
    count = sum(r['VerticesWithRemovedInfluences'] for r in report['Meshes'])
    loss = max((r['MaximumRemovedFraction'] for r in report['Meshes']), default=0)
    return f'Cleanup: {count} vertices lost influences; largest removal {loss:.1%}. Original untouched. Check poses, then Export selected character. See Weight cleanup report.'


def _mksm_reduce_copies(context, originals, target, deviation_percent, weld=False):
    """Reduce new mesh copies; measure sampled surface deviation in world units."""
    import bmesh
    import math
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    if not originals: raise ValueError('Select the replacement mesh objects first.')
    counts = []
    for source in originals:
        if any(not math.isfinite(c) for v in source.data.vertices for c in v.co):
            raise ValueError(f'{source.name}: non-finite coordinates must be repaired first.')
        if source.data.shape_keys:
            raise ValueError(f'{source.name}: apply the intended shape and remove shape keys first.')
        if any(m.type != 'ARMATURE' and (m.show_viewport or m.show_render) for m in source.modifiers):
            raise ValueError(f'{source.name}: apply existing mesh modifiers first. Keep the Armature modifier.')
        source.data.calc_loop_triangles(); counts.append(len(source.data.loop_triangles))
        if not counts[-1]: raise ValueError(f'{source.name}: no faces to reduce.')
        if abs(source.matrix_world.determinant()) < 1e-12:
            raise ValueError(f'{source.name}: zero object scale cannot be reduced.')
    total = sum(counts)
    collection = bpy.data.collections.new('MKSM Geometry Preview')
    context.scene.collection.children.link(collection)
    copies = []; rows = []
    selected = list(context.selected_objects); active = context.view_layer.objects.active
    try:
        for source, count in zip(originals, counts):
            obj = source.copy(); obj.data = source.data.copy()
            copies.append(obj); collection.objects.link(obj)
            obj.name = source.name + '_Reduced'; obj.hide_viewport = False
            obj.hide_select = False; obj.hide_render = False; obj.hide_set(False)
            for key in ('mksm_prepared_id', 'mksm_chunk', 'mksm_grouped'):
                if key in obj: del obj[key]
            # An edited replacement must not masquerade as a topology-preserving export.
            for attr in list(obj.data.attributes):
                if attr.name.startswith('_MKSM_'): obj.data.attributes.remove(attr)
            _mksm_select(context, [obj])
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bm = bmesh.new()
            try:
                bm.from_mesh(obj.data)
                if weld:
                    # Reconnect only effectively coincident points with equal paint.
                    # Material and UV boundaries remain stored per face corner.
                    layer = bm.verts.layers.deform.active; seen = {}; mapping = {}
                    for v in bm.verts:
                        paint = tuple(sorted((k, round(w, 6)) for k, w in v[layer].items() if w > 0)) if layer else ()
                        key = (tuple(round(c, 6) for c in v.co), paint)
                        if key in seen and (v.co - seen[key].co).length <= 1e-6:
                            mapping[v] = seen[key]
                        else: seen[key] = v
                    if mapping: bmesh.ops.weld_verts(bm, targetmap=mapping)
                loose = [v for v in bm.verts if not v.link_faces]
                if loose: bmesh.ops.delete(bm, geom=loose, context='VERTS')
                bmesh.ops.triangulate(bm, faces=list(bm.faces), quad_method='BEAUTY', ngon_method='BEAUTY')
                bm.to_mesh(obj.data)
            finally: bm.free()
            obj.data.validate(clean_customdata=True); obj.data.update(); obj.data.calc_loop_triangles()
            points = [v.co.copy() for v in obj.data.vertices]
            faces = [tuple(t.vertices) for t in obj.data.loop_triangles]
            original_tree = BVHTree.FromPolygons(points, faces, all_triangles=True)
            low = Vector([min(p[i] for p in points) for i in range(3)])
            high = Vector([max(p[i] for p in points) for i in range(3)])
            diagonal = (high-low).length
            if not original_tree or diagonal < 1e-12: raise ValueError(f'{source.name}: empty/degenerate surface.')
            # No strong regional collapse masks: these can shred thin geometry.
            budget = max(4, int(target * count / total))
            ratio = min(1.0, budget / len(faces))
            modifier = obj.modifiers.new('MKSM Geometry Reduction', 'DECIMATE')
            modifier.decimate_type = 'COLLAPSE'; modifier.ratio = ratio
            modifier.use_collapse_triangulate = True
            while obj.modifiers.find(modifier.name) > 0:
                bpy.ops.object.modifier_move_up(modifier=modifier.name)
            bpy.ops.object.modifier_apply(modifier=modifier.name)
            bm = bmesh.new()
            try:
                bm.from_mesh(obj.data)
                bmesh.ops.triangulate(bm, faces=list(bm.faces), quad_method='BEAUTY', ngon_method='BEAUTY')
                bm.to_mesh(obj.data)
            finally: bm.free()
            obj.data.validate(clean_customdata=True); obj.data.update(); obj.data.calc_loop_triangles()
            after_points = [v.co.copy() for v in obj.data.vertices]
            after_faces = [tuple(t.vertices) for t in obj.data.loop_triangles]
            reduced_tree = BVHTree.FromPolygons(after_points, after_faces, all_triangles=True)
            if not after_faces or not reduced_tree: raise ValueError(f'{source.name}: reduction removed the surface; use a higher budget.')
            # Vertices plus face centers, both directions. This is a sample bound,
            # not a Hausdorff proof or a guarantee of animation/UV fidelity.
            def distances(vertices, triangles, tree):
                for point in vertices:
                    hit = tree.find_nearest(point)
                    if hit[0] is None: raise ValueError('Surface comparison failed.')
                    yield hit[3]
                for triangle in triangles:
                    point = sum((vertices[i] for i in triangle), Vector()) / 3
                    hit = tree.find_nearest(point)
                    if hit[0] is None: raise ValueError('Surface comparison failed.')
                    yield hit[3]
            error = max(max(distances(points, faces, reduced_tree)), max(distances(after_points, after_faces, original_tree)))
            if not math.isfinite(error): raise ValueError('Non-finite reduction geometry.')
            error_percent = error / diagonal * 100
            if error_percent > deviation_percent + 1e-6:
                raise ValueError(f'{source.name}: sampled surface change {error_percent:.2f}% exceeds {deviation_percent:.2f}%. Increase triangle budget or allowed deviation. Original unchanged.')
            # Blender interpolates deform weights when collapsing edges. Normalize
            # retained paint; never silently perform native palette cleanup here.
            arms = [m for m in obj.modifiers if m.type == 'ARMATURE' and m.object]
            bone_names = set(arms[0].object.data.bones.keys()) if len(arms) == 1 else set()
            names = {g.index:g.name for g in obj.vertex_groups}
            palettes = []; unweighted = 0; max_influences = 0
            for v in obj.data.vertices:
                row = {g.group:g.weight for g in v.groups if g.weight > 0 and names[g.group] in bone_names}
                value = sum(row.values())
                if bone_names and not value: unweighted += 1
                if value:
                    for index, weight in row.items(): obj.vertex_groups[index].add([v.index], weight/value, 'REPLACE')
                palettes.append(set(row)); max_influences = max(max_influences, len(row))
            if unweighted: raise ValueError(f'{source.name}: {unweighted} vertices have no game bone weights.')
            incompatible = sum(len(set().union(*(palettes[i] for i in t))) > 3 for t in after_faces) if bone_names else 0
            rows.append({'SourceMesh':source.name, 'PreviewMesh':obj.name,
                         'VerticesBefore':len(source.data.vertices), 'TrianglesBefore':count,
                         'VerticesAfter':len(after_points), 'TrianglesAfter':len(after_faces),
                         'AllocatedTriangleBudget':budget, 'BudgetMet':len(after_faces)<=budget,
                         'SampledSurfaceChangePercent':error_percent, 'SampledSurfaceChangeWorldUnits':error,
                         'MaximumBoneInfluences':max_influences, 'IncompatibleNativeTriangles':incompatible,
                         'UVLayers':len(obj.data.uv_layers), 'Materials':len(obj.data.materials)})
        return copies, collection, {'Method':'Blender geometric edge collapse on copies; optional equal-weight seam welding; bidirectional vertex/face-center surface samples.',
                                   'TriangleTarget':target, 'AllowedSurfaceChangePercent':deviation_percent,
                                   'TotalTrianglesAfter':sum(row['TrianglesAfter'] for row in rows),
                                   'CombinedBudgetMet':sum(row['TrianglesAfter'] for row in rows)<=target,
                                   'NativeWeightCleanupApplied':False, 'GameplayTested':False,
                                   'Meshes':rows, 'OriginalMeshesAndRigUnchanged':True}
    except Exception:
        _mksm_remove_cleanup(copies, collection); raise
    finally:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected:
            if obj.name in context.view_layer.objects: obj.select_set(True)
        context.view_layer.objects.active = active


class MKSM_OT_reduce_preview(bpy.types.Operator):
    bl_idname = 'mksm.reduce_preview'
    bl_label = 'Preview reduced geometry on copies'
    bl_description = 'Reduce selected meshes without changing originals or rig. Reject excessive sampled surface deviation; review textures and poses before export'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        if context.object and context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Switch to Object Mode first.'); return {'CANCELLED'}
        originals = [o for o in context.selected_objects if o.type == 'MESH']
        try:
            copies, collection, report = _mksm_reduce_copies(context, originals,
                context.scene.mksm_reduction_triangles, context.scene.mksm_reduction_deviation,
                context.scene.mksm_reduction_weld)
        except Exception as exc:
            self.report({'ERROR'}, str(exc)); return {'CANCELLED'}
        collection['mksm_reduction_sources'] = json.dumps([{ 'name':o.name, 'hidden':o.hide_get(), 'render':o.hide_render} for o in originals])
        collection['mksm_reduction_preview'] = True
        for obj in originals: obj.hide_set(True); obj.hide_render = True
        _mksm_select(context, copies)
        block = bpy.data.texts.new('MKSM Geometry Reduction Report'); block.write(json.dumps(report, indent=2))
        context.scene.mksm_reduction_report = block.name
        triangles = sum(r['TrianglesAfter'] for r in report['Meshes'])
        conflicts = sum(r['IncompatibleNativeTriangles'] for r in report['Meshes'])
        met = '' if report['CombinedBudgetMet'] else ' Target not met; some meshes cannot collapse further.'
        self.report({'INFO'}, f'Preview: {triangles} triangles; {conflicts} native weight conflicts.{met} Original unchanged. Check poses/textures; see Geometry reduction report.')
        return {'FINISHED'}


class MKSM_OT_reduce_discard(bpy.types.Operator):
    bl_idname = 'mksm.reduce_discard'
    bl_label = 'Discard selected reduction preview'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        collections = {c for o in context.selected_objects for c in o.users_collection if c.get('mksm_reduction_preview')}
        if not collections:
            self.report({'ERROR'}, 'Select a reduced preview mesh first.'); return {'CANCELLED'}
        restored = []
        for collection in collections:
            for row in json.loads(collection['mksm_reduction_sources']):
                source = context.scene.objects.get(row['name'])
                if source:
                    source.hide_set(row['hidden']); source.hide_render = row['render']; restored.append(source)
            _mksm_remove_cleanup(list(collection.objects), collection)
        _mksm_select(context, [o for o in restored if not o.hide_get()])
        return {'FINISHED'}


class MKSM_OT_reduce_report(bpy.types.Operator):
    bl_idname = 'mksm.reduce_report'
    bl_label = 'Geometry reduction report'
    def invoke(self, context, event):
        if not bpy.data.texts.get(context.scene.mksm_reduction_report):
            self.report({'ERROR'}, 'Create a reduction preview first.'); return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=560)
    def draw(self, context):
        report = json.loads(bpy.data.texts[context.scene.mksm_reduction_report].as_string())
        _mksm_lines(self.layout, f"Combined triangles: {report['TotalTrianglesAfter']} / target {report['TriangleTarget']}.")
        for row in report['Meshes']:
            _mksm_lines(self.layout, row['PreviewMesh'],
                f"Triangles: {row['TrianglesBefore']} -> {row['TrianglesAfter']}; vertices: {row['VerticesBefore']} -> {row['VerticesAfter']}",
                f"Sampled surface change: {row['SampledSurfaceChangePercent']:.2f}% of mesh diagonal.",
                f"Native weight conflicts: {row['IncompatibleNativeTriangles']}. Budget {'met' if row['BudgetMet'] else 'not met' }.")
        _mksm_lines(self.layout, 'Inspect silhouette, UV seams and joint poses. Weight cleanup is a separate opt-in step.',
            'GLB seams and native draw batches can add vertices. Studio compiled counts are authoritative.',
            'This does not raise game memory limits. Full details in Text Editor:', context.scene.mksm_reduction_report)
    def execute(self, context): return {'FINISHED'}


def _mksm_bone_suggestion(name, target_names):
    """Conservative aliases; ambiguous root/cloth bones require user mapping."""
    import re
    if name in target_names: return [(name, 1.0)]
    key = re.sub(r'[^a-z0-9]', '', name.split(':')[-1].lower())
    aliases = {'hips':'pelvis','pelvis':'pelvis','spine':'abdomen','spine2':'chest','chest':'chest',
               'neck':'neck','head':'head'}
    if key == 'spine1' and {'abdomen','chest'} <= target_names:
        return [('abdomen', .5), ('chest', .5)]
    if name.startswith('F_') and 'head' in target_names: return [('head', 1.0)]
    if key in aliases and aliases[key] in target_names: return [(aliases[key],1.0)]
    for side, long_side in [('l','left'),('r','right')]:
        for source, dest in [('shoulder','clavicle'),('arm','shoulder'),('upperarm','shoulder'),
                             ('armroll','bicep'),('forearm','forearm'),('lowerarm','forearm'),
                             ('forearmroll','forearm'),('hand','hand'),('upleg','thigh'),
                             ('uplegroll','thigh'),('thigh','thigh'),('leg','calf'),
                             ('legroll','calf'),('calf','calf'),('foot','foot'),('toebase','toe')]:
            if key in (long_side+source,side+source,source+side,'valvebipedbip01'+side+source):
                target = side+'_'+dest
                return [(target,1.0)] if target in target_names else []
        valve = 'valvebipedbip01'+side+'finger'
        if key.startswith(valve):
            suffix = key[len(valve):]
            if suffix and suffix[0] in '01234':
                digit = 'thumb' if suffix[0]=='0' else 'finger' if suffix[0] in '12' else 'pinky'
                target = side+'_'+digit+('00' if len(suffix)==1 else '01')
                return [(target,1.0)] if target in target_names else []
        for digit, dest in [('thumb','thumb'),('index','finger'),('middle','finger'),('ring','pinky'),('pinky','pinky')]:
            prefix=long_side+'hand'+digit
            if key.startswith(prefix) and key[len(prefix):] in ('1','2','3','4'):
                target=side+'_'+dest+('00' if key[len(prefix):]=='1' else '01')
                return [(target,1.0)] if target in target_names else []
    return []


def _mksm_retarget_copies(context, originals, source_rig, target_rig, mapping, fit):
    import math, statistics, bmesh
    from mathutils import Vector, Matrix
    if not originals: raise ValueError('Select your new character meshes.')
    if not source_rig or not target_rig or source_rig == target_rig:
        raise ValueError('Choose separate source and original game skeletons.')
    if source_rig.type != 'ARMATURE' or target_rig.type != 'ARMATURE' or not target_rig.get('mksm_source_sha256'):
        raise ValueError('The destination must be an original MKSM Studio skeleton.')
    for rig in (source_rig, target_rig):
        if abs(rig.matrix_world.determinant()) < 1e-12: raise ValueError('A skeleton has zero scale.')
        if rig.data.pose_position != 'REST' and any(abs(b.matrix_basis[i][j]-(1 if i==j else 0))>1e-5 for b in rig.pose.bones for i in range(4) for j in range(4)):
            raise ValueError('Set both skeletons to Rest Position before retargeting. Existing poses are not changed.')
    used = set(); source_rows = {}
    for obj in originals:
        arms = [m for m in obj.modifiers if m.type == 'ARMATURE']
        if len(arms)!=1 or arms[0].object != source_rig:
            raise ValueError(f'{obj.name}: bind this mesh to the chosen source skeleton first.')
        if obj.data.shape_keys or any(m.type!='ARMATURE' and (m.show_viewport or m.show_render) for m in obj.modifiers):
            raise ValueError(f'{obj.name}: apply mesh modifiers and intended shape keys first.')
        rows=[]
        for v in obj.data.vertices:
            if any(not math.isfinite(c) for c in v.co): raise ValueError('Non-finite source coordinates.')
            row={obj.vertex_groups[g.group].name:g.weight for g in v.groups if g.weight>0 and obj.vertex_groups[g.group].name in source_rig.data.bones}
            if not row: raise ValueError(f'{obj.name}: vertex {v.index} has no source bone weights.')
            if any(not math.isfinite(w) for w in row.values()):raise ValueError('Non-finite source weights.')
            total=sum(row.values());row={k:w/total for k,w in row.items()}
            used.update(row);rows.append(row)
        source_rows[obj.name]=rows
    missing=sorted(name for name in used if not mapping.get(name))
    if missing: raise ValueError('Map these weighted bones first: '+', '.join(missing[:10])+(' ...' if len(missing)>10 else ''))
    for name in used:
        row=mapping[name]
        if any(target not in target_rig.data.bones or not math.isfinite(weight) or weight<=0 for target,weight in row):
            raise ValueError(f'{name}: choose valid destination bones and positive weights.')
        if abs(sum(w for _,w in row)-1)>1e-5: raise ValueError(f'{name}: mapped weights must sum to 1.')
    mapping=dict(mapping)
    for bone in source_rig.data.bones:
        if bone.name not in mapping:
            suggestion=_mksm_bone_suggestion(bone.name,set(target_rig.data.bones.keys()))
            if suggestion:mapping[bone.name]=suggestion
    source_heads={b.name:source_rig.matrix_world@b.head_local for b in source_rig.data.bones}
    target_heads={b.name:target_rig.matrix_world@b.head_local for b in target_rig.data.bones}
    # Helpers mapped to the same bone share an anchor with their ancestor.
    # Facial/roll helpers must not collapse independently onto the target head.
    primary={}
    for name in sorted(source_rig.data.bones.keys(),key=lambda n:0 if _mksm_bone_suggestion(n,set(target_heads))==mapping.get(n) else 1):
        row=mapping.get(name,[])
        if len(row)==1 and row[0][1]==1:primary.setdefault(row[0][0],name)
    anchors={}
    def anchor(name):
        if name in anchors:return anchors[name]
        parent=source_rig.data.bones[name].parent
        if not parent and len(mapping.get(name,[]))==1 and primary.get(mapping[name][0][0],name)!=name:
            result=primary[mapping[name][0][0]]
        elif parent and mapping.get(parent.name)==mapping.get(name): result=anchor(parent.name)
        else:result=name
        anchors[name]=result;return result
    for name in used:anchor(name)
    scale=1.0
    if fit:
        ratios=[]
        pairs=[('pelvis','head'),('l_shoulder','l_forearm'),('r_shoulder','r_forearm'),('l_thigh','l_calf'),('r_thigh','r_calf')]
        for a,b in pairs:
            if a not in primary or b not in primary:continue
            source_delta=source_heads[primary[b]]-source_heads[primary[a]]
            target_delta=target_heads[b]-target_heads[a]
            if min(source_delta.length,target_delta.length)<1e-6:continue
            angle=math.degrees(source_delta.angle(target_delta))
            if angle>25:raise ValueError(f'Rest poses differ around {a} ({angle:.0f} degrees). Align the source rest pose with the game skeleton, or fit manually and disable Fit Proportions.')
            ratios.append(target_delta.length/source_delta.length)
        if len(ratios)<2:raise ValueError('Fit Proportions needs at least two mapped main-body segments. Complete pelvis/head and limb mapping, or fit manually.')
        scale=statistics.median(ratios)
        if not math.isfinite(scale) or not .0001<scale<10000:raise ValueError('Invalid source-to-game scale.')
    offsets={name:sum((target_heads[n]*w for n,w in mapping[anchor(name)]),Vector())-source_heads[anchor(name)]*scale for name in used}
    collection=bpy.data.collections.new('MKSM Retarget Preview');context.scene.collection.children.link(collection)
    copies=[];report=[]
    try:
        for original in originals:
            obj=original.copy();obj.data=original.data.copy();copies.append(obj);collection.objects.link(obj)
            obj.name=original.name+'_MKSM';obj.hide_viewport=False;obj.hide_select=False;obj.hide_render=False;obj.hide_set(False)
            world=original.matrix_world.copy();obj.parent=None;obj.matrix_world=Matrix.Identity(4)
            obj.modifiers.clear();obj.vertex_groups.clear()
            for key in list(obj.keys()):
                if key.startswith('mksm_'):del obj[key]
            for attr in list(obj.data.attributes):
                if attr.name.startswith('_MKSM_'):obj.data.attributes.remove(attr)
            obj['mksm_source_sha256']=target_rig['mksm_source_sha256'];obj['mksm_vertex_type']=2
            rows=[];max_move=0
            for v,source_row in zip(obj.data.vertices,source_rows[original.name]):
                point=world@v.co
                fitted=point*scale+sum((offsets[n]*w for n,w in source_row.items()),Vector()) if fit else point
                if any(not math.isfinite(c) for c in fitted):raise ValueError('Invalid fitted coordinate.')
                max_move=max(max_move,(fitted-point*scale).length);v.co=fitted
                mapped={}
                for source,w in source_row.items():
                    for target,fraction in mapping[source]:mapped[target]=mapped.get(target,0)+w*fraction
                for target,value in mapped.items():
                    group=obj.vertex_groups.get(target) or obj.vertex_groups.new(name=target)
                    group.add([v.index],value,'REPLACE')
                rows.append(set(mapped))
            bm=bmesh.new()
            try:
                bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data)
            finally:bm.free()
            obj.data.update();obj.data.calc_loop_triangles()
            modifier=obj.modifiers.new('MKSM Game Skeleton','ARMATURE');modifier.object=target_rig
            obj.parent=target_rig;obj.matrix_parent_inverse=target_rig.matrix_world.inverted();obj.matrix_basis=Matrix.Identity(4)
            conflicts=sum(len(set().union(*(rows[i] for i in triangle.vertices)))>3 for triangle in obj.data.loop_triangles)
            report.append({'SourceMesh':original.name,'PreviewMesh':obj.name,'Vertices':len(obj.data.vertices),'Triangles':len(obj.data.loop_triangles),
                           'MaximumFitOffset':max_move,'IncompatibleNativeTriangles':conflicts})
        collection['mksm_retarget_sources']=json.dumps([{'name':o.name,'hidden':o.hide_get(),'render':o.hide_render} for o in originals])
        return copies,collection,{'SourceRig':source_rig.name,'GameRig':target_rig.name,'Scale':scale,'FitProportions':fit,
                                 'BoneMap':{n:mapping[n] for n in sorted(used)},'Meshes':report,'OriginalsUnchanged':True,
                                 'NativeWeightCleanupApplied':False,'GameTested':False}
    except Exception:
        _mksm_remove_cleanup(copies,collection);raise


class MKSM_RetargetMap(bpy.types.PropertyGroup):
    source_name: StringProperty(name='Source bone')
    target_name: StringProperty(name='Game bone')
    second_target: StringProperty(name='Optional second bone')
    second_weight: FloatProperty(name='Second bone share',default=.5,min=.01,max=.99)


class MKSM_UL_retarget_map(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row=layout.row(align=True);row.label(text=item.source_name,icon='BONE_DATA' if item.target_name else 'ERROR')
        rig=context.scene.mksm_target_rig
        if rig:row.prop_search(item,'target_name',rig.data,'bones',text='')
        else:row.prop(item,'target_name',text='')


class MKSM_OT_match_bones(bpy.types.Operator):
    bl_idname='mksm.match_bones';bl_label='Match Bones';bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        scene=context.scene;source=scene.mksm_source_rig;target=scene.mksm_target_rig
        if not source or not target or source==target:
            self.report({'ERROR'},'Choose source and game skeletons first.');return {'CANCELLED'}
        selected=[o for o in context.selected_objects if o.type=='MESH']
        used={o.vertex_groups[g.group].name for o in selected for v in o.data.vertices for g in v.groups if g.weight>0 and o.vertex_groups[g.group].name in source.data.bones}
        if not used:self.report({'ERROR'},'Select weighted source meshes first.');return {'CANCELLED'}
        previous={r.source_name:(r.target_name,r.second_target,r.second_weight) for r in scene.mksm_bone_map} if scene.mksm_map_source==source.name and scene.mksm_map_target==target.name else {}
        scene.mksm_bone_map.clear()
        for name in sorted(used):
            row=scene.mksm_bone_map.add();row.source_name=name
            suggestion=_mksm_bone_suggestion(name,set(target.data.bones.keys()))
            if name in previous:
                row.target_name,row.second_target,row.second_weight=previous[name]
            elif suggestion:
                row.target_name=suggestion[0][0]
                if len(suggestion)>1:row.second_target=suggestion[1][0];row.second_weight=suggestion[1][1]
        scene.mksm_map_source=source.name;scene.mksm_map_target=target.name
        missing=sum(not r.target_name for r in scene.mksm_bone_map)
        self.report({'INFO'},f'{len(used)-missing}/{len(used)} bones matched. {missing} need review. Check left/right and helper bones.');return {'FINISHED'}


class MKSM_OT_retarget_preview(bpy.types.Operator):
    bl_idname='mksm.retarget_preview';bl_label='Create Retarget Preview';bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        scene=context.scene
        if context.object and context.object.mode!='OBJECT':self.report({'ERROR'},'Switch to Object Mode.');return {'CANCELLED'}
        if not scene.mksm_source_rig or not scene.mksm_target_rig or scene.mksm_map_source!=scene.mksm_source_rig.name or scene.mksm_map_target!=scene.mksm_target_rig.name:
            self.report({'ERROR'},'Click Match Bones for the selected skeletons first.');return {'CANCELLED'}
        mapping={r.source_name:([(r.target_name,1-r.second_weight),(r.second_target,r.second_weight)] if r.second_target else [(r.target_name,1)]) if r.target_name else [] for r in scene.mksm_bone_map}
        originals=[o for o in context.selected_objects if o.type=='MESH']
        try:copies,collection,report=_mksm_retarget_copies(context,originals,scene.mksm_source_rig,scene.mksm_target_rig,mapping,scene.mksm_retarget_fit)
        except Exception as ex:self.report({'ERROR'},str(ex));return {'CANCELLED'}
        for obj in originals:obj.hide_set(True);obj.hide_render=True
        _mksm_select(context,copies)
        block=bpy.data.texts.new('MKSM Retarget Report');block.write(json.dumps(report,indent=2));scene.mksm_retarget_report=block.name
        conflicts=sum(r['IncompatibleNativeTriangles'] for r in report['Meshes'])
        self.report({'INFO'},f'Preview created. {conflicts} native weight conflicts; check shoulders, elbows, hips and head before export.');return {'FINISHED'}


class MKSM_OT_retarget_discard(bpy.types.Operator):
    bl_idname='mksm.retarget_discard';bl_label='Discard Retarget Preview';bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        groups={c for o in context.selected_objects for c in o.users_collection if 'mksm_retarget_sources' in c}
        if not groups:self.report({'ERROR'},'Select a retarget preview mesh.');return {'CANCELLED'}
        sources=[]
        for group in groups:
            for row in json.loads(group['mksm_retarget_sources']):
                obj=context.scene.objects.get(row['name'])
                if obj:obj.hide_set(row['hidden']);obj.hide_render=row['render'];sources.append(obj)
            _mksm_remove_cleanup(list(group.objects),group)
        _mksm_select(context,[o for o in sources if not o.hide_get()]);return {'FINISHED'}


class MKSM_OT_retarget_report(bpy.types.Operator):
    bl_idname='mksm.retarget_report';bl_label='Retarget Report'
    def invoke(self,context,event):
        if not bpy.data.texts.get(context.scene.mksm_retarget_report):self.report({'ERROR'},'Create a retarget preview first.');return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self,width=540)
    def draw(self,context):
        report=json.loads(bpy.data.texts[context.scene.mksm_retarget_report].as_string())
        _mksm_lines(self.layout,f"{report['SourceRig']} -> {report['GameRig']}",f"Fit scale: {report['Scale']:.4f}")
        for row in report['Meshes']:_mksm_lines(self.layout,row['PreviewMesh'],f"{row['Vertices']} vertices; {row['IncompatibleNativeTriangles']} native weight conflicts.")
        _mksm_lines(self.layout,'Original meshes and skeletons unchanged. Preview shoulders, elbows, hips and head.',
                    'Review original head and special-move attachments separately. Retargeting does not remove or restore native records.',
                    'Full mapping in Text Editor: '+context.scene.mksm_retarget_report)
    def execute(self,context):return {'FINISHED'}


def _mksm_game_rigs(context):
    target = getattr(context.scene, 'mksm_target_rig', None)
    if target and target.name in context.scene.objects and target.type == 'ARMATURE' and target.get('mksm_source_sha256'):
        return [target]
    return [o for o in context.scene.objects if o.type == 'ARMATURE' and o.get('mksm_source_sha256')]


class MKSM_OT_cleanup_preview(bpy.types.Operator):
    bl_idname = 'mksm.cleanup_preview'
    bl_label = 'Preview cleaned weights on a copy'
    bl_description = 'Clean selected meshes on new copies; keep the original mesh and skeleton unchanged. Check poses before exporting'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        if context.object and context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Switch to Object Mode first.'); return {'CANCELLED'}
        originals = [o for o in context.selected_objects if o.type == 'MESH']
        rigs = _mksm_game_rigs(context)
        if not originals or len(rigs) != 1:
            self.report({'ERROR'}, 'Select the new body meshes in a scene with one original game skeleton.'); return {'CANCELLED'}
        try:
            copies, collection, report = _mksm_cleanup_copies(context, originals, rigs[0])
            message = _mksm_save_cleanup_report(context, report)
            for obj in originals: obj.hide_set(True)
            _mksm_select(context, copies)
        except Exception as exc:
            self.report({'ERROR'}, str(exc)); return {'CANCELLED'}
        self.report({'INFO'}, message); return {'FINISHED'}


class MKSM_OT_cleanup_report(bpy.types.Operator):
    bl_idname = 'mksm.cleanup_report'
    bl_label = 'Weight cleanup report'
    def invoke(self, context, event):
        if not bpy.data.texts.get(context.scene.mksm_cleanup_report):
            self.report({'ERROR'}, 'Run cleanup preview or export with cleanup enabled first.'); return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=560)
    def draw(self, context):
        report = json.loads(bpy.data.texts[context.scene.mksm_cleanup_report].as_string())
        for row in report['Meshes']:
            _mksm_lines(self.layout, row['SourceMesh'], f"{row['IncompatibleTrianglesBefore']} incompatible triangles -> 0",
                        f"{row['VerticesWithRemovedInfluences']} vertices lost influences. Largest removal: {row['MaximumRemovedFraction']:.1%}.")
        _mksm_lines(self.layout, 'Original weights untouched. Pose the cleaned copy and check joints.',
                    'Full before/after weights are in the Text Editor:', context.scene.mksm_cleanup_report,
                    'This fixes weight compatibility, not game memory limits or loading freezes.')
    def execute(self, context): return {'FINISHED'}


class MKSM_OT_replacement(bpy.types.Operator, ExportHelper):
    bl_idname = 'mksm.export_replacement'
    bl_label = 'Export character (.glb)'
    filename_ext = '.glb'
    filter_glob: StringProperty(default='*.glb', options={'HIDDEN'})
    selected_only: BoolProperty(name='Export selected meshes only', description='Select the new body AND any extra skinned parts you need, such as the dragon. The original skeleton is included automatically.', default=False)
    def execute(self, context):
        if context.object and context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Switch to Object Mode before exporting.')
            return {'CANCELLED'}
        rigs = _mksm_game_rigs(context)
        if len(rigs) != 1:
            self.report({'ERROR'}, 'Use one original Studio armature per replacement scene.')
            return {'CANCELLED'}
        rig = rigs[0]
        meshes = [o for o in (context.selected_objects if self.selected_only else context.scene.objects) if o.type == 'MESH' and (('mksm_chunk' not in o and not o.get('mksm_grouped')) or o.get('mksm_vertex_type') == 2) and any(m.type == 'ARMATURE' and m.object == rig for m in o.modifiers)]
        if not meshes:
            self.report({'ERROR'}, 'Bind the replacement meshes to the original Studio armature first.')
            return {'CANCELLED'}
        if any(m.type != 'ARMATURE' and (m.show_viewport or m.show_render) for o in meshes for m in o.modifiers):
            self.report({'ERROR'}, 'Apply mesh modifiers before exporting the replacement. Keep the Armature modifier.')
            return {'CANCELLED'}
        if any(o.data.shape_keys for o in meshes):
            self.report({'ERROR'}, 'Apply the intended shape and remove shape keys before exporting.')
            return {'CANCELLED'}
        if any(not o.data.uv_layers or not o.data.materials for o in meshes):
            self.report({'ERROR'}, 'Every replacement mesh needs UVs and an original Studio material.')
            return {'CANCELLED'}
        selected = list(context.selected_objects); active = context.view_layer.objects.active
        objects = meshes + [rig]
        hidden = {o:(o.hide_get(),o.hide_viewport,o.hide_select) for o in objects}
        copies = []; collection = None; cleanup_report = None
        try:
            if context.scene.mksm_auto_cleanup:
                copies, collection, cleanup_report = _mksm_cleanup_copies(context, meshes, rig)
                objects = copies + [rig]
            bpy.ops.object.select_all(action='DESELECT')
            for o in objects:
                o.hide_viewport=False; o.hide_set(False); o.hide_select=False; o.select_set(True)
            result=bpy.ops.export_scene.gltf(filepath=self.filepath, export_format='GLB', use_selection=True, export_attributes=True, export_extras=True, export_skins=True, export_animations=False, export_apply=False, export_def_bones=False, export_rest_position_armature=True, export_yup=True)
            if result == {'FINISHED'} and cleanup_report is not None:
                cleanup_report['ExportFile'] = self.filepath
                _mksm_save_cleanup_report(context, cleanup_report)
                Path(self.filepath + '.weights.json').write_text(json.dumps(cleanup_report, indent=2), encoding='utf-8')
        except Exception as exc:
            self.report({'ERROR'}, str(exc)); return {'CANCELLED'}
        finally:
            bpy.ops.object.select_all(action='DESELECT')
            _mksm_remove_cleanup(copies, collection)
            for o,(local,view,select) in hidden.items():
                o.hide_set(local); o.hide_viewport=view; o.hide_select=select
            for o in selected:o.select_set(True)
            context.view_layer.objects.active=active
        if result == {'FINISHED'} and cleanup_report is not None:
            count = sum(r['VerticesWithRemovedInfluences'] for r in cleanup_report['Meshes'])
            self.report({'INFO'}, f'Saved GLB with cleaned export weights ({count} vertices lost influences). Original untouched. See Weight cleanup report and the .weights.json beside the GLB.')
        elif result == {'FINISHED'}:
            self.report({'INFO'}, 'Saved GLB. In Studio: same character > Import character > choose GLB > Build ISO.')
        return result


class MKSM_OT_object(bpy.types.Operator, ExportHelper):
    bl_idname = 'mksm.export_object'
    bl_label = 'Export selected weapon / object (.glb)'
    filename_ext = '.glb'
    filter_glob: StringProperty(default='*.glb', options={'HIDDEN'})
    def execute(self, context):
        if context.object and context.object.mode != 'OBJECT':
            self.report({'ERROR'}, 'Switch to Object Mode before exporting.'); return {'CANCELLED'}
        meshes = [o for o in context.selected_objects if o.type == 'MESH']
        if not meshes:
            self.report({'ERROR'}, 'Select the replacement weapon/object meshes.'); return {'CANCELLED'}
        if any(o.data.shape_keys or any(m.show_viewport or m.show_render for m in o.modifiers) for o in meshes):
            self.report({'ERROR'}, 'Apply mesh modifiers and shape keys first. Rigid objects do not need an armature.'); return {'CANCELLED'}
        sources = {o.get('mksm_source_sha256') for o in context.scene.objects if o.get('mksm_source_sha256')}
        if len(sources) != 1:
            self.report({'ERROR'}, 'Start with one destination object exported by Studio. Keep its source properties.'); return {'CANCELLED'}
        if any(not o.data.uv_layers or not o.data.materials or any(m is None or 'mksm_material_id' not in m for m in o.data.materials) for o in meshes):
            self.report({'ERROR'}, 'Every object needs UVs and the original destination Studio materials.'); return {'CANCELLED'}
        selected=list(context.selected_objects);active=context.view_layer.objects.active
        saved={o:('mksm_source_sha256' in o,o.get('mksm_source_sha256')) for o in meshes}
        try:
            bpy.ops.object.select_all(action='DESELECT')
            for o in meshes:o['mksm_source_sha256']=next(iter(sources));o.select_set(True)
            result=bpy.ops.export_scene.gltf(filepath=self.filepath,export_format='GLB',use_selection=True,export_attributes=True,export_extras=True,export_skins=False,export_animations=False,export_apply=False,export_yup=True)
        finally:
            for o,(existed,value) in saved.items():
                if existed:o['mksm_source_sha256']=value
                elif 'mksm_source_sha256' in o:del o['mksm_source_sha256']
            bpy.ops.object.select_all(action='DESELECT')
            for o in selected:o.select_set(True)
            context.view_layer.objects.active=active
        self.report({'INFO'}, 'Studio: select the destination > Import weapon / object > Import Blender object > Add to project > Build ISO.')
        return result

class MKSM_OT_native_character(bpy.types.Operator, ExportHelper):
    bl_idname = 'mksm.export_native_character'
    bl_label = 'Export game character (.mksmcharacter)'
    filename_ext = '.mksmcharacter'
    filter_glob: StringProperty(default='*.mksmcharacter', options={'HIDDEN'})
    def execute(self, context):
        exe = bpy.path.abspath(context.scene.mksm_studio_exe)
        source = bpy.path.abspath(context.scene.mksm_native_source)
        if not Path(exe).is_file() or not Path(source).is_file():
            self.report({'ERROR'}, 'Open Game-format export below. Choose MKSM Studio.exe and the ORIGINAL .original.pme2 file saved by Studio.')
            return {'CANCELLED'}
        if Path(self.filepath).exists():
            self.report({'ERROR'}, 'Choose a new character filename; existing exports are preserved.')
            return {'CANCELLED'}
        try:
            with tempfile.TemporaryDirectory(prefix='mksm-character-') as temp:
                glb = str(Path(temp) / 'replacement.glb')
                exported = bpy.ops.mksm.export_replacement(filepath=glb, selected_only=True)
                if 'FINISHED' not in exported:
                    return {'CANCELLED'}
                result = subprocess.run([exe, '--build-character', source, glb, self.filepath], capture_output=True, text=True, timeout=180, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                if result.returncode:
                    error = Path(glb + '.error.txt')
                    message = error.read_text(encoding='utf-8-sig') if error.is_file() else result.stderr
                    self.report({'ERROR'}, (message.splitlines()[0] if message else 'Native compilation failed.'))
                    return {'CANCELLED'}
                if not Path(self.filepath).is_file():
                    raise RuntimeError('Studio did not create the native character package.')
                if context.scene.mksm_auto_cleanup:
                    report = bpy.data.texts.get(context.scene.mksm_cleanup_report)
                    if report: Path(self.filepath + '.weights.json').write_text(report.as_string(), encoding='utf-8')
        except (OSError, subprocess.TimeoutExpired, RuntimeError) as exc:
            self.report({'ERROR'}, str(exc))
            return {'CANCELLED'}
        self.report({'INFO'}, 'Saved .mksmcharacter. In Studio: choose the same character > Import character > choose this file > Build ISO.')
        return {'FINISHED'}

class MKSM_OT_animation(bpy.types.Operator, ExportHelper):
    bl_idname = 'mksm.export_animation'
    bl_label = 'Export edited animation (.glb)'
    filename_ext = '.glb'
    filter_glob: StringProperty(default='*.glb', options={'HIDDEN'})
    def execute(self, context):
        rigs=[o for o in context.scene.objects if o.type=='ARMATURE' and o.get('mksm_source_sha256')]
        if len(rigs)!=1 or not rigs[0].animation_data or not rigs[0].animation_data.action:
            self.report({'ERROR'},'Choose one original Studio rig with an active action. Open a single-clip Studio export first.')
            return {'CANCELLED'}
        scene=context.scene
        if scene.frame_start!=0 or scene.frame_end<0 or scene.frame_end>=65535:
            self.report({'ERROR'},'Use frame 0 as the start and an end frame below 65535.')
            return {'CANCELLED'}
        rig=rigs[0];ad=rig.animation_data
        if any(not track.mute for track in ad.nla_tracks):
            self.report({'ERROR'},'Mute NLA tracks and select the edited action before exporting.')
            return {'CANCELLED'}
        if context.object and context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
        objects=[rig]+[o for o in context.scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==rig for m in o.modifiers)]
        if len(objects)==1:
            self.report({'ERROR'},'Keep the original skinned model with the animation rig.')
            return {'CANCELLED'}
        selected=list(context.selected_objects);active=context.view_layer.objects.active
        hidden={o:(o.hide_get(),o.hide_viewport,o.hide_select) for o in objects}
        timing={'mksm_animation_fps':scene.render.fps/scene.render.fps_base,'mksm_animation_start':scene.frame_start,'mksm_animation_end':scene.frame_end}
        saved_timing={key:(key in rig,rig.get(key)) for key in timing}
        try:
            for key,value in timing.items():rig[key]=value
            bpy.ops.object.select_all(action='DESELECT')
            for o in objects:o.hide_viewport=False;o.hide_set(False);o.hide_select=False;o.select_set(True)
            result=bpy.ops.export_scene.gltf(filepath=self.filepath,export_format='GLB',use_selection=True,export_extras=True,export_skins=True,export_animations=True,export_force_sampling=True,export_frame_range=True,export_animation_mode='ACTIVE_ACTIONS',export_def_bones=False,export_rest_position_armature=True,export_yup=True,export_materials='NONE')
        except Exception as exc:
            self.report({'ERROR'},str(exc));return {'CANCELLED'}
        finally:
            for key,(existed,value) in saved_timing.items():
                if existed:rig[key]=value
                elif key in rig:del rig[key]
            bpy.ops.object.select_all(action='DESELECT')
            for o,(local,view,select) in hidden.items():o.hide_set(local);o.hide_viewport=view;o.hide_select=select
            for o in selected:o.select_set(True)
            context.view_layer.objects.active=active
        self.report({'INFO'},'Animation Lab: choose the original clip > Import edited clip > preview > Add animation to project. Enable Use Blender timing for length changes or new keys; Higher precision reduces packed animation rounding. Keep the same FPS and start at frame 0.')
        return result

import struct
import hashlib
import uuid

def _mksm_template(scene, rig, all_slots=False):
    source = Path(bpy.path.abspath(scene.mksm_native_source))
    template = Path(bpy.path.abspath(scene.mksm_template_glb)) if scene.mksm_template_glb else Path(str(source).replace('.original.pme2', '.glb'))
    if not source.is_file() or not template.is_file():
        raise ValueError('Click Open original MKSM model first. Keep the GLB and its .original.pme2 file in the same folder.')
    digest = hashlib.sha256(source.read_bytes()).hexdigest().upper()
    if str(rig.get('mksm_source_sha256', '')).upper() != digest:
        raise ValueError('The native source belongs to a different rig. Open the correct destination Studio GLB.')
    raw = template.read_bytes()
    if len(raw) < 20 or raw[:4] != b'glTF':
        raise ValueError('The destination template must be a Studio GLB.')
    chunks = {}; pos = 12
    while pos + 8 <= len(raw):
        size, kind = struct.unpack_from('<II', raw, pos); pos += 8
        if pos + size > len(raw): raise ValueError('Truncated destination GLB.')
        chunks[kind] = raw[pos:pos + size]; pos += size
    doc = json.loads(chunks[0x4E4F534A]); binary = chunks[0x004E4942]
    if str(doc.get('asset', {}).get('extras', {}).get('mksm_source_sha256', '')).upper() != digest:
        raise ValueError('The template GLB and original native source do not match.')
    used = set(); attachment_textures = set()
    for node in doc.get('nodes', []):
        if 'mesh' in node and 'skin' in node:
            for primitive in doc['meshes'][node['mesh']]['primitives']:
                if 'material' in primitive: used.add(primitive['material'])
    for node in doc.get('nodes', []):
        if 'mesh' in node and 'skin' not in node:
            for primitive in doc['meshes'][node['mesh']]['primitives']:
                if 'material' in primitive:
                    attachment_textures.add(doc['materials'][primitive['material']].get('extras', {}).get('mksm_texture_index', -1))
    slots = []
    for index in sorted(used):
        material = doc['materials'][index]; extra = material.get('extras', {})
        if 'mksm_material_id' not in extra or extra.get('mksm_texture_index', -1) < 0: continue
        texture = material.get('pbrMetallicRoughness', {}).get('baseColorTexture')
        if texture is None: continue
        image = doc['images'][doc['textures'][texture['index']]['source']]
        if 'bufferView' not in image: continue
        view = doc['bufferViews'][image['bufferView']]; start = view.get('byteOffset', 0)
        data = binary[start:start + view['byteLength']]
        if data[:8] != b'\x89PNG\r\n\x1a\n' or len(data) < 24: continue
        width, height = struct.unpack_from('>II', data, 16)
        if 16 <= width <= 4096 and 16 <= height <= 4096:
            slots.append((width * height, -int(extra['mksm_material_id']), width, height, extra))
    if not slots: raise ValueError('No textured native body material found. Export the destination with its textures loaded.')
    if all_slots: return digest, slots, attachment_textures
    _, _, width, height, extra = max(slots, key=lambda s: (s[0], s[1]))
    return digest, width, height, extra, extra['mksm_texture_index'] in attachment_textures

def _mksm_base_shader(material):
    if material is None or not material.use_nodes:
        raise ValueError('Every used material must use a Principled BSDF base-color shader.')
    nodes = material.node_tree.nodes
    outputs = [n for n in nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output]
    links = list(outputs[0].inputs['Surface'].links) if outputs else []
    if len(links) != 1 or links[0].from_node.type != 'BSDF_PRINCIPLED':
        raise ValueError(f'{material.name}: use a Principled BSDF directly connected to Material Output. Special shaders need manual preparation.')
    shader = links[0].from_node
    if shader.inputs['Alpha'].is_linked or shader.inputs['Alpha'].default_value < 0.9999:
        raise ValueError(f'{material.name}: automatic preparation supports opaque materials only. Disconnect unused Alpha links or prepare transparency manually.')
    for node in nodes:
        if node.type == 'TEX_IMAGE' and node.image is not None and not node.image.has_data:
            # Packed/file images are loaded lazily after opening a .blend.
            # Access the buffer before treating an unloaded image as missing.
            try: _ = node.image.pixels[0]
            except (IndexError, RuntimeError): pass
        if node.type == 'TEX_IMAGE' and (node.image is None or node.image.source not in {'FILE', 'GENERATED'} or not node.image.has_data):
            raise ValueError(f'{material.name}: a texture is missing, unreadable, tiled or animated. Load a regular image first.')
    return shader, outputs[0]

def _mksm_select(context, objects):
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects: obj.select_set(True)
    context.view_layer.objects.active = objects[0] if objects else None

def _mksm_prepare(context):
    # Keep older button/operator calls working without the old single-atlas bake.
    return _mksm_prepare_textures(context)


def _mksm_texture_input(material, obj):
    shader, _ = _mksm_base_shader(material)
    base = shader.inputs['Base Color']
    uv_name = next((uv.name for uv in obj.data.uv_layers if uv.active_render), obj.data.uv_layers.active.name)
    if not base.is_linked:
        color = tuple(base.default_value)
        return ('color', color), None, color, uv_name
    link = base.links[0]; node = link.from_node
    if node.type != 'TEX_IMAGE' or link.from_socket.name != 'Color' or node.projection != 'FLAT':
        raise ValueError(f'{material.name}: connect one Image Texture directly to Base Color first. Mixed/procedural shaders need a baked color image.')
    if node.inputs['Vector'].is_linked:
        uv_link = node.inputs['Vector'].links[0]; uv_node = uv_link.from_node
        if uv_node.type == 'UVMAP':
            uv_name = uv_node.uv_map or uv_name
        elif not (uv_node.type == 'TEX_COORD' and uv_link.from_socket.name == 'UV'):
            raise ValueError(f'{material.name}: apply texture Mapping nodes to the UVs first.')
    if uv_name not in obj.data.uv_layers:
        raise ValueError(f'{material.name}: UV map {uv_name} is missing.')
    if node.extension != 'REPEAT':
        raise ValueError(f'{material.name}: automatic image packing currently needs Image Texture extension Repeat.')
    if node.image.colorspace_settings.name != 'sRGB':
        raise ValueError(f'{material.name}: use an sRGB color image for automatic texture setup.')
    return ('image', node.image.as_pointer()), node.image, None, uv_name


def _mksm_tile_rectangles(items, width, height):
    # Partition pixel space, not individual UV islands. Each source image keeps
    # its own layout; repeated/overlapping UVs within that image remain valid.
    result = {}
    def split(rows, x, y, w, h):
        if len(rows) == 1:
            if min(w, h) < 8: raise ValueError('Too many images for these texture slots. Increase Game textures or simplify the materials.')
            result[rows[0]['key']] = (x, y, w, h); return
        total = sum(r['area'] for r in rows); acc = 0; cut = 1
        for i, row in enumerate(rows[:-1], 1):
            acc += row['area']; cut = i
            if acc >= total / 2: break
        ratio = sum(r['area'] for r in rows[:cut]) / total
        if w >= h:
            size = max(4, min(w - 4, round(w * ratio)))
            split(rows[:cut], x, y, size, h); split(rows[cut:], x + size, y, w - size, h)
        else:
            size = max(4, min(h - 4, round(h * ratio)))
            split(rows[:cut], x, y, w, size); split(rows[cut:], x, y + size, w, h - size)
    split(items, 0, 0, width, height)
    return result


def _mksm_prepare_textures(context):
    import numpy as np
    if context.object and context.object.mode != 'OBJECT': raise ValueError('Switch to Object Mode first.')
    scene = context.scene
    rigs = _mksm_game_rigs(context)
    if len(rigs) != 1: raise ValueError('Use one original Studio skeleton in this scene.')
    rig = rigs[0]; originals = [o for o in context.selected_objects if o.type == 'MESH']
    if not originals: raise ValueError('Select your NEW body meshes first. Leave the dragon and other parts unselected.')
    digest, available, protected = _mksm_template(scene, rig, all_slots=True)
    # Unselected native meshes are kept parts, including skinned extras. Reserve
    # their slots even when hidden. Never guess from names such as "dragon".
    retained = []; previous_backups = set()
    previous = bpy.data.texts.get(scene.mksm_prepare_report)
    if previous:
        try:
            old = json.loads(previous.as_string())
            selected_names = {o.name for o in originals}
            if old.get('Source') == digest and (selected_names.intersection(old.get('OriginalMeshes', [])) or
                    any(o.get('mksm_prepared_id') == old.get('PreparedToken') for o in originals if old.get('PreparedToken'))):
                previous_backups.update(old.get('BackupMeshes', old.get('OriginalMeshes', []))); previous_backups.update(old.get('Meshes', []))
        except (ValueError, TypeError): pass
    for obj in scene.objects:
        if obj in originals or obj.name in previous_backups or obj.type != 'MESH' or str(obj.get('mksm_source_sha256', '')).upper() != digest: continue
        ids = {obj.data.materials[p.material_index].get('mksm_texture_index', -1)
               for p in obj.data.polygons if p.material_index < len(obj.data.materials) and obj.data.materials[p.material_index]}
        protected.update(i for i in ids if i >= 0); retained.append(obj.name)
    slots = [s for s in available if s[4]['mksm_texture_index'] not in protected]
    # Different native materials can alias the same image slot.
    unique = {}
    for slot in sorted(slots, key=lambda s: (-s[0], -s[1])): unique.setdefault(slot[4]['mksm_texture_index'], slot)
    slots = list(unique.values())
    if not slots:
        raise ValueError('All game textures are used by unselected original meshes. Save a backup, remove only the old body after weight transfer, and keep needed extras. Then select your NEW body.')
    inputs = {}; face_sources = {}; bone_names = set(rig.data.bones.keys())
    for obj in originals:
        arms = [m for m in obj.modifiers if m.type == 'ARMATURE']
        if len(arms) != 1 or arms[0].object != rig: raise ValueError(f'{obj.name}: use the original skeleton in the Armature modifier.')
        if not obj.data.uv_layers: raise ValueError(f'{obj.name}: the new body needs its original UV map.')
        if obj.data.shape_keys or any(m.type != 'ARMATURE' and (m.show_render or m.show_viewport) for m in obj.modifiers):
            raise ValueError(f'{obj.name}: apply mesh modifiers and shape keys first; keep the Armature modifier.')
        influences = [{obj.vertex_groups[g.group].name for g in v.groups if g.weight > 0.000001 and obj.vertex_groups[g.group].name in bone_names} for v in obj.data.vertices]
        if any(not g for g in influences): raise ValueError(f'{obj.name}: some vertices have no weights on the original bones.')
        obj.data.calc_loop_triangles()
        if not scene.mksm_auto_cleanup and any(len(set().union(*(influences[v] for v in t.vertices))) > 3 for t in obj.data.loop_triangles):
            raise ValueError(f'{obj.name}: a triangle touches more than 3 bones. Enable Clean weights on export or use Preview cleaned weights on a copy. Texture setup itself leaves weights unchanged.')
        for index in sorted({p.material_index for p in obj.data.polygons}):
            if index >= len(obj.data.materials): raise ValueError(f'{obj.name}: a face has no material.')
            mat = obj.data.materials[index]
            key, image, color, uv = _mksm_texture_input(mat, obj)
            row = inputs.setdefault(key, {'key': key, 'image': image, 'color': color, 'area': max(1, image.size[0] * image.size[1]) if image else 1, 'preferred': set(), 'materials': []})
            row['preferred'].add(mat.get('mksm_texture_index', -1)); row['materials'].append(mat.name)
            face_sources[(obj, index)] = (key, uv)
    # UV domains may live in negative tiles or repeat beyond 0..1. Capture the
    # used domain per source image, and resample that periodic image domain.
    for row in inputs.values(): row['domain'] = [float('inf'), float('inf'), -float('inf'), -float('inf')]
    for obj in originals:
        for poly in obj.data.polygons:
            key, uv_name = face_sources[(obj, poly.material_index)]; domain = inputs[key]['domain']
            for loop in poly.loop_indices:
                u, v = obj.data.uv_layers[uv_name].data[loop].uv
                if not np.isfinite(u) or not np.isfinite(v): raise ValueError(f'{obj.name}: UV coordinates must be finite.')
                domain[0] = min(domain[0], u); domain[1] = min(domain[1], v)
                domain[2] = max(domain[2], u); domain[3] = max(domain[3], v)
    for row in inputs.values():
        d = row['domain']; d[2] = max(d[2], d[0] + .000001); d[3] = max(d[3], d[1] + .000001)
        row['area'] *= max(1, d[2] - d[0]) * max(1, d[3] - d[1])
    rows = sorted(inputs.values(), key=lambda r: -r['area'])
    count = min(len(slots), len(rows), scene.mksm_texture_count or len(slots))
    # Preserve existing native slot assignments when possible before filling
    # unused slots. This keeps already-correct characters predictable.
    chosen = []
    for row in rows:
        candidate = next((s for s in slots if s not in chosen and s[4]['mksm_texture_index'] in row['preferred']), None)
        if candidate and len(chosen) < count: chosen.append(candidate)
    chosen += [s for s in slots if s not in chosen][:count - len(chosen)]
    buckets = [[] for _ in chosen]
    for row in rows:
        empty_preferred = next((i for i, s in enumerate(chosen) if not buckets[i] and s[4]['mksm_texture_index'] in row['preferred']), None)
        i = empty_preferred if empty_preferred is not None else min(range(count), key=lambda i: sum(r['area'] for r in buckets[i]) / chosen[i][0])
        buckets[i].append(row)
    placement = {}; plans = []
    for slot, bucket in zip(chosen, buckets):
        width, height = slot[2:4]; rects = _mksm_tile_rectangles(bucket, width, height)
        for row in bucket:
            x, y, w, h = rects[row['key']]; pad = 2 if len(bucket) > 1 else 0
            placement[row['key']] = (len(plans), (x + pad, y + pad, w - 2 * pad, h - 2 * pad), len(bucket) > 1)
        plans.append((slot, bucket, rects))
    selected = list(context.selected_objects); active = context.view_layer.objects.active
    hidden = {o: o.hide_get() for o in originals}; copies = []; meshes = []; materials = []; images = []; collection = None; report = None; done = False
    token = uuid.uuid4().hex; summary = []
    try:
        collection = bpy.data.collections.new('MKSM Prepared Textures'); scene.collection.children.link(collection)
        for slot, bucket, rects in plans:
            width, height, native = slot[2:]; texture_id = native['mksm_texture_index']
            if len(bucket) == 1 and bucket[0]['image']:
                atlas = bucket[0]['image'].copy(); images.append(atlas)
                if tuple(atlas.size) != (width, height): atlas.scale(width, height)
            else:
                atlas = bpy.data.images.new(f'MKSM Game Texture {texture_id}', width=width, height=height, alpha=False); images.append(atlas)
                atlas.colorspace_settings.name = 'sRGB'
                pixels = np.zeros((height, width, 4), dtype=np.float32); pixels[:, :, 3] = 1
                for row in bucket:
                    x, y, w, h = rects[row['key']]; _, (ix, iy, iw, ih), _ = placement[row['key']]
                    if row['image']:
                        source = row['image']; sw, sh = source.size
                        data = np.empty(sw * sh * 4, dtype=np.float32); source.pixels.foreach_get(data); data = data.reshape(sh, sw, 4)
                        # Center-aligned bilinear sampling; duplicate edge pixels
                        # into the gutter to prevent adjacent-tile color bleed.
                        du, dv, eu, ev = row['domain']
                        us = np.clip((np.arange(w) + x - ix + .5) / iw, .5 / iw, 1 - .5 / iw)
                        vs = np.clip((np.arange(h) + y - iy + .5) / ih, .5 / ih, 1 - .5 / ih)
                        xs = np.mod((du + us * (eu - du)) * sw - .5, sw)
                        ys = np.mod((dv + vs * (ev - dv)) * sh - .5, sh)
                        x0 = xs.astype(int); y0 = ys.astype(int); fx = (xs - x0)[None, :, None]; fy = (ys - y0)[:, None, None]
                        top = data[y0[:, None], x0[None, :]] * (1 - fx) + data[y0[:, None], ((x0 + 1) % sw)[None, :]] * fx
                        bottom = data[((y0 + 1) % sh)[:, None], x0[None, :]] * (1 - fx) + data[((y0 + 1) % sh)[:, None], ((x0 + 1) % sw)[None, :]] * fx
                        pixels[y:y+h, x:x+w] = top * (1 - fy) + bottom * fy
                    else: pixels[y:y+h, x:x+w] = row['color']
                pixels[:, :, 3] = 1; atlas.pixels.foreach_set(pixels.ravel()); atlas.update()
            atlas.name = f'MKSM Game Texture {texture_id}'; atlas.pack()
            material = bpy.data.materials.new(f'MKSM texture {texture_id}'); materials.append(material); material.use_nodes = True
            for key, value in native.items():
                if key.startswith('mksm_'): material[key] = value
            shader = next(n for n in material.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
            shader.inputs['Metallic'].default_value = 0; shader.inputs['Roughness'].default_value = 1
            texture = material.node_tree.nodes.new('ShaderNodeTexImage'); texture.image = atlas
            material.node_tree.links.new(texture.outputs['Color'], shader.inputs['Base Color'])
            summary.append({'TextureIndex': texture_id, 'MaterialId': native['mksm_material_id'], 'Size': [width, height], 'Inputs': [r['materials'] for r in bucket], 'Tiles': [list(placement[r['key']][1]) for r in bucket], 'SourceUVDomains': [r['domain'] for r in bucket]})
        for source in originals:
            obj = source.copy(); obj.data = source.data.copy(); meshes.append(obj.data); copies.append(obj); collection.objects.link(obj)
            obj.name = source.name + '_GameTextures'; obj.hide_viewport = False; obj.hide_select = False; obj.hide_render = False; obj.hide_set(False)
            obj['mksm_source_sha256'] = digest; obj['mksm_vertex_type'] = 2; obj['mksm_prepared_id'] = token
            target = obj.data.uv_layers.new(name='MKSM_Game_UV')
            for poly in obj.data.polygons:
                key, uv_name = face_sources[(source, poly.material_index)]; index, (x, y, w, h), packed = placement[key]
                width, height = plans[index][0][2:4]
                for loop in poly.loop_indices:
                    u, v = source.data.uv_layers[uv_name].data[loop].uv
                    du, dv, eu, ev = inputs[key]['domain']
                    target.data[loop].uv = ((x + (u - du) / (eu - du) * w) / width, (y + (v - dv) / (ev - dv) * h) / height) if packed else (u, v)
                poly.material_index = index
            target_name = target.name
            for uv in list(obj.data.uv_layers):
                if uv.name != target_name: obj.data.uv_layers.remove(uv)
            obj.data.uv_layers.active_index = 0; obj.data.uv_layers[0].active_render = True
            # Color attributes would multiply the new base-color image in GLB.
            for attribute in list(obj.data.color_attributes): obj.data.color_attributes.remove(attribute)
            indices = [p.material_index for p in obj.data.polygons]
            obj.data.materials.clear()
            for material in materials: obj.data.materials.append(material)
            for poly, index in zip(obj.data.polygons, indices): poly.material_index = index
        report = bpy.data.texts.new('MKSM Texture Setup Report')
        report.write(json.dumps({'Status': 'Texture setup checked; gameplay not tested', 'Source': digest, 'PreparedToken': token, 'Meshes': [o.name for o in copies], 'OriginalMeshes': [o.name for o in originals], 'BackupMeshes': sorted(previous_backups.union(o.name for o in originals)), 'Textures': summary, 'ProtectedTextureSlots': sorted(protected), 'KeptMeshes': retained, 'Method': 'Copy images to native slots; combine image rectangles only when necessary. No UV unwrap or Cycles bake.', 'Preserved': 'Source objects untouched; copied positions, topology, weights, transforms and native part metadata unchanged.', 'Review': 'Native-size images may lose detail when reduced. Normal maps and other shader effects are not exported. Keep required extras when exporting. Test in game.'}, indent=2))
        for obj in originals: obj.hide_set(True)
        _mksm_select(context, copies)
        scene.mksm_prepared_id = token; scene.mksm_prepare_report = report.name; done = True
        return f'Ready: {len(images)} game textures. Original meshes kept. Check the copy; export it with needed extras.'
    finally:
        if not done:
            for obj in copies: bpy.data.objects.remove(obj, do_unlink=True)
            for mesh in meshes:
                if mesh.users == 0: bpy.data.meshes.remove(mesh)
            for material in materials:
                if material.users == 0: bpy.data.materials.remove(material)
            for atlas in images:
                if atlas.users == 0: bpy.data.images.remove(atlas)
            if report: bpy.data.texts.remove(report)
            if collection: bpy.data.collections.remove(collection)
            for obj, value in hidden.items(): obj.hide_set(value)
            _mksm_select(context, selected); context.view_layer.objects.active = active


class MKSM_OT_prepare_textures(bpy.types.Operator):
    bl_idname = 'mksm.prepare_textures'
    bl_label = 'Set up game textures (keep more detail)'
    bl_description = 'Use several original texture slots. Keep source UV layouts; combine images only when necessary. Does not edit weights or original meshes'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try: message = _mksm_prepare_textures(context)
        except Exception as exc:
            self.report({'ERROR'}, str(exc)); return {'CANCELLED'}
        self.report({'INFO'}, message); return {'FINISHED'}


class MKSM_OT_prepare(bpy.types.Operator):
    bl_idname = 'mksm.prepare_character'
    bl_label = 'Set up game textures (legacy shortcut)'
    bl_description = 'Use the current multi-texture helper; kept for older shortcuts'
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        try: message = _mksm_prepare(context)
        except Exception as exc:
            self.report({'ERROR'}, str(exc)); return {'CANCELLED'}
        self.report({'INFO'}, message); return {'FINISHED'}

class MKSM_OT_prepared_export(bpy.types.Operator, ExportHelper):
    bl_idname = 'mksm.export_prepared'
    bl_label = 'Export prepared body (.glb)'
    filename_ext = '.glb'
    filter_glob: StringProperty(default='*.glb', options={'HIDDEN'})
    def execute(self, context):
        token = context.scene.mksm_prepared_id
        objects = [o for o in context.scene.objects if token and o.type == 'MESH' and o.get('mksm_prepared_id') == token]
        if not objects:
            self.report({'ERROR'}, 'Click Set up game textures first. Then check the result before export.'); return {'CANCELLED'}
        selected = list(context.selected_objects); active = context.view_layer.objects.active
        hidden = {o: (o.hide_get(), o.hide_viewport, o.hide_select) for o in objects}
        try:
            for o in objects: o.hide_set(False); o.hide_viewport = False; o.hide_select = False
            _mksm_select(context, objects)
            return bpy.ops.mksm.export_replacement(filepath=self.filepath, selected_only=True)
        finally:
            bpy.ops.object.select_all(action='DESELECT')
            for o, (local, view, select) in hidden.items(): o.hide_set(local); o.hide_viewport = view; o.hide_select = select
            for o in selected: o.select_set(True)
            context.view_layer.objects.active = active

class MKSM_OT_prepare_report(bpy.types.Operator):
    bl_idname = 'mksm.prepare_report'
    bl_label = 'Check texture result'
    def invoke(self, context, event):
        if not bpy.data.texts.get(context.scene.mksm_prepare_report):
            self.report({'ERROR'}, 'Click Set up game textures first. Then check the result before export.'); return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=560)
    def draw(self, context):
        report = json.loads(bpy.data.texts[context.scene.mksm_prepare_report].as_string())
        if 'Textures' in report:
            self.layout.label(text=f"Prepared {len(report['Meshes'])} meshes with {len(report['Textures'])} game textures")
            for texture in report['Textures']:
                self.layout.label(text=f"Slot {texture['TextureIndex']}: {texture['Size'][0]} x {texture['Size'][1]} | {len(texture['Inputs'])} source images/colors")
            self.layout.label(text='Protected slots: ' + ', '.join(map(str, report['ProtectedTextureSlots'])))
        else:
            self.layout.label(text=f"Prepared {len(report['Meshes'])} meshes - {report['AtlasSize'][0]} x {report['AtlasSize'][1]} atlas")
            self.layout.label(text=f"Native texture {report['TextureIndex']} - material {report['MaterialId']}")
        self.layout.label(text='Original meshes kept; selected source meshes hidden in viewport.')
        self.layout.label(text='Prepared copies retain positions, topology and bone weights.')
        self.layout.label(text='Review texture detail and seams before saving.')
        if report.get('SharedWithAttachments'):
            self.layout.label(text='This texture is shared with native attachments/extra meshes.', icon='ERROR')
            self.layout.label(text='Their old UVs remain; they may need manual texture work.')
        self.layout.label(text='Opaque base color only. Other shader effects are not recreated.')
        self.layout.label(text='Studio converts the palette. Test the rebuilt ISO in game.')
        self.layout.label(text='Full details saved in Text Editor: ' + context.scene.mksm_prepare_report)
    def execute(self, context):
        return {'FINISHED'}

class MKSM_OT_start_here(bpy.types.Operator):
    bl_idname = 'mksm.start_here'
    bl_label = 'Read the simple guide'
    bl_description = 'Open the step-by-step character guide on GitHub'
    def execute(self, context):
        bpy.ops.wm.url_open(url='https://github.com/OGmidway/Mortal-Kombat-Shaolin-Monks-Modding-Tool/blob/main/docs/CHARACTER_START_HERE.md')
        return {'FINISHED'}

def _mksm_lines(layout, *lines):
    col = layout.column(align=True)
    region = bpy.context.region
    scale = bpy.context.preferences.system.ui_scale
    width = max(22, int((region.width - 52 * scale) / (7 * scale))) if region else 52
    for line in lines:
        for part in textwrap.wrap(line, width=width): col.label(text=part)

class MKSM_PT_bridge(bpy.types.Panel):
    bl_label='MKSM Bridge 0.26.0';bl_idname='MKSM_PT_bridge';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='MKSM'
    def draw(self,context):
        self.layout.operator('mksm.import_model',text='Open Game Character',icon='IMPORT')
        self.layout.operator('mksm.start_here',text='Workflow Help',icon='HELP')
        self.layout.label(text='By OG Midway')
        self.layout.label(text='Contributors: RelaxDirk · Z mods')


class MKSM_PT_character(bpy.types.Panel):
    bl_label='1. Retarget Character';bl_idname='MKSM_PT_character';bl_parent_id='MKSM_PT_bridge';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='MKSM'
    def draw(self,context):
        scene=context.scene;layout=self.layout
        layout.prop(scene,'mksm_source_rig');layout.prop(scene,'mksm_target_rig')
        layout.operator('mksm.match_bones',icon='ARMATURE_DATA')
        if scene.mksm_bone_map:
            missing=sum(not r.target_name for r in scene.mksm_bone_map)
            layout.label(text=f'{len(scene.mksm_bone_map)-missing}/{len(scene.mksm_bone_map)} matched · {missing} to review',icon='ERROR' if missing else 'CHECKMARK')
            layout.template_list('MKSM_UL_retarget_map','',scene,'mksm_bone_map',scene,'mksm_bone_map_index',rows=4)
            if 0<=scene.mksm_bone_map_index<len(scene.mksm_bone_map):
                row=scene.mksm_bone_map[scene.mksm_bone_map_index]
                layout.prop(scene,'mksm_show_blend_map',text='Blend Two Game Bones',icon='TRIA_DOWN' if scene.mksm_show_blend_map else 'TRIA_RIGHT',emboss=False)
                if scene.mksm_show_blend_map and scene.mksm_target_rig:
                    layout.prop_search(row,'second_target',scene.mksm_target_rig.data,'bones',text='Second Bone')
                    if row.second_target:layout.prop(row,'second_weight',text='Second Share')
        layout.prop(scene,'mksm_retarget_fit')
        layout.operator('mksm.retarget_preview',icon='MOD_ARMATURE')
        row=layout.row(align=True);row.operator('mksm.retarget_report',text='Report',icon='TEXT');row.operator('mksm.retarget_discard',text='Discard',icon='TRASH')
        _mksm_lines(layout,'Select source meshes. Match bones, then preview movement. Already on game rig? Skip this step.')


class MKSM_PT_geometry(bpy.types.Panel):
    bl_label='2. Reduce Geometry';bl_idname='MKSM_PT_geometry';bl_parent_id='MKSM_PT_bridge';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='MKSM';bl_options={'DEFAULT_CLOSED'}
    def draw(self,context):
        layout=self.layout;scene=context.scene
        layout.prop(scene,'mksm_reduction_triangles',text='Triangle Budget')
        layout.prop(scene,'mksm_reduction_deviation',text='Surface Change (%)')
        layout.prop(scene,'mksm_reduction_weld',text='Reconnect Matching Seams')
        layout.operator('mksm.reduce_preview',text='Create Reduction Preview',icon='MOD_DECIM')
        row=layout.row(align=True);row.operator('mksm.reduce_report',text='Report',icon='TEXT');row.operator('mksm.reduce_discard',text='Discard',icon='TRASH')
        _mksm_lines(layout,'Check silhouette and joints. Final game counts can be higher than Blender counts.')


class MKSM_PT_materials(bpy.types.Panel):
    bl_label='3. Prepare Textures';bl_idname='MKSM_PT_materials';bl_parent_id='MKSM_PT_bridge';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='MKSM';bl_options={'DEFAULT_CLOSED'}
    def draw(self,context):
        layout=self.layout
        layout.prop(context.scene,'mksm_texture_count',text='Texture Slots (0 = Auto)')
        layout.operator('mksm.prepare_textures',text='Prepare Game Textures',icon='TEXTURE')
        layout.operator('mksm.prepare_report',text='Texture Report',icon='TEXT')
        _mksm_lines(layout,'Select new body only. Keep required native extras separate. Already mapped? Skip.')


class MKSM_PT_export_character(bpy.types.Panel):
    bl_label='4. Check & Export';bl_idname='MKSM_PT_export_character';bl_parent_id='MKSM_PT_bridge';bl_space_type='VIEW_3D';bl_region_type='UI';bl_category='MKSM';bl_options={'DEFAULT_CLOSED'}
    def draw(self,context):
        layout=self.layout;scene=context.scene
        layout.prop(scene,'mksm_auto_cleanup',text='Clean Weights on Export')
        layout.prop(scene,'mksm_cleanup_max_loss',text='Max Weight Removed (%)')
        layout.operator('mksm.cleanup_preview',text='Preview Weight Cleanup',icon='MOD_VERTEX_WEIGHT')
        layout.operator('mksm.cleanup_report',text='Weight Report',icon='TEXT')
        op=layout.operator('mksm.export_replacement',text='Export Selected Character (.glb)',icon='EXPORT');op.selected_only=True
        layout.operator('mksm.export_prepared',text='Export Prepared Body (.glb)',icon='EXPORT')
        _mksm_lines(layout,'Select new body + needed skinned extras. Check original head and spear/dragon parts in Studio. Import Character, then test in game.')


class MKSM_PT_native(bpy.types.Panel):
    bl_label = 'Optional: game-format export (.mksmcharacter)'
    bl_idname = 'MKSM_PT_native'
    bl_parent_id = 'MKSM_PT_bridge'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MKSM'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        _mksm_lines(self.layout, 'Use this instead of GLB export if you need',
                    'a game-format character package.',
                    'Select new body + needed skinned extras first.')
        self.layout.label(text='MKSM Studio program goes here:')
        self.layout.prop(context.scene, 'mksm_studio_exe', text='Studio .exe')
        self.layout.label(text='UNTOUCHED Shaolin Monks model goes here:')
        self.layout.prop(context.scene, 'mksm_native_source', text='Original .pme2')
        _mksm_lines(self.layout, 'Use the .original.pme2 saved by Studio.',
                    'This is NOT your new character or .blend file.',
                    'Keep its .textures.bin companion beside it.')
        self.layout.operator('mksm.export_native_character', icon='EXPORT')
        _mksm_lines(self.layout, 'Studio: Import character > choose this file.',
                    'Review > Build ISO > test in PCSX2.')

class MKSM_PT_other(bpy.types.Panel):
    bl_label = 'Other jobs: shape, weapon or animation'
    bl_idname = 'MKSM_PT_other'
    bl_parent_id = 'MKSM_PT_bridge'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MKSM'
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        box = self.layout.box()
        box.label(text='Only moved the original vertices or UVs?')
        _mksm_lines(box, 'Keep the original bones, weights and faces.',
                    'Use this for shape edits, not a new body.')
        box.operator('mksm.export_edits', icon='EXPORT')
        box.label(text='Studio: Import Blender edits.')
        box = self.layout.box()
        box.label(text='Replacing a weapon or a rigid object?')
        _mksm_lines(box, 'Select the NEW object meshes.',
                    'Keep game materials and the grip position.')
        box.operator('mksm.export_object', icon='EXPORT')
        box.label(text='Studio: Import weapon / object.')
        box = self.layout.box()
        box.label(text='Changed an animation?')
        _mksm_lines(box, 'Keep the game rig. Pick your edited action.',
                    'Start at frame 0. Keep the exported FPS.',
                    'Mute other NLA tracks before export.')
        box.operator('mksm.export_animation', icon='ACTION')
        _mksm_lines(box, 'Studio Animation Lab: Import edited clip.',
                    'Changed length or keys? Use Blender timing.',
                    'Preview > Add animation to project > Build ISO.')

classes=(MKSM_RetargetMap,MKSM_UL_retarget_map,MKSM_OT_match_bones,MKSM_OT_retarget_preview,MKSM_OT_retarget_discard,MKSM_OT_retarget_report,MKSM_OT_reduce_preview,MKSM_OT_reduce_discard,MKSM_OT_reduce_report,MKSM_OT_cleanup_preview,MKSM_OT_cleanup_report,MKSM_OT_import,MKSM_OT_export,MKSM_OT_replacement,MKSM_OT_object,MKSM_OT_native_character,MKSM_OT_animation,MKSM_OT_prepare,MKSM_OT_prepare_textures,MKSM_OT_prepared_export,MKSM_OT_prepare_report,MKSM_OT_start_here,MKSM_PT_bridge,MKSM_PT_character,MKSM_PT_geometry,MKSM_PT_materials,MKSM_PT_export_character,MKSM_PT_native,MKSM_PT_other)
def register():
    # Register the PropertyGroup before the CollectionProperty references it.
    bpy.utils.register_class(MKSM_RetargetMap)
    bpy.types.Scene.mksm_source_rig = PointerProperty(name='Source Skeleton', type=bpy.types.Object, poll=lambda self,obj:obj.type=='ARMATURE')
    bpy.types.Scene.mksm_target_rig = PointerProperty(name='Game Skeleton', type=bpy.types.Object, poll=lambda self,obj:obj.type=='ARMATURE' and bool(obj.get('mksm_source_sha256')))
    bpy.types.Scene.mksm_bone_map = CollectionProperty(type=MKSM_RetargetMap)
    bpy.types.Scene.mksm_bone_map_index = IntProperty(default=0)
    bpy.types.Scene.mksm_map_source = StringProperty()
    bpy.types.Scene.mksm_map_target = StringProperty()
    bpy.types.Scene.mksm_retarget_fit = BoolProperty(name='Fit Proportions', description='Optional joint-guided fitting for similarly aligned rest poses. Creates preview copies. Disable if you fitted the model manually. Check joints and overlapping clothing', default=False)
    bpy.types.Scene.mksm_show_blend_map = BoolProperty(default=False)
    bpy.types.Scene.mksm_retarget_report = StringProperty()
    bpy.types.Scene.mksm_reduction_triangles = IntProperty(name='Triangle budget (selected meshes)', description='Combined target across selected replacement meshes. Native batching and UV seams can add exported vertices; verify final counts in Studio', default=4000, min=4, max=1000000)
    bpy.types.Scene.mksm_reduction_deviation = FloatProperty(name='Allowed surface change (%)', description='Reject if sampled bidirectional vertex/face-center distance exceeds this fraction of the source bounding-box diagonal. Not a guarantee for animation or textures', default=1.0, min=0.01, max=25, precision=2)
    bpy.types.Scene.mksm_reduction_weld = BoolProperty(name='Reconnect equal-weight seams', description='Optional: weld effectively coincident vertices only when bone weights agree. UV/material boundaries remain per face corner. Inspect seams after reduction', default=False)
    bpy.types.Scene.mksm_reduction_report = StringProperty()
    bpy.types.Scene.mksm_auto_cleanup = BoolProperty(name='Clean weights on export', description='Optional: create temporary copies, fix triangles touching more than three bones, normalize native weights, then export. Original meshes stay untouched. Preview joints after cleanup', default=False)
    bpy.types.Scene.mksm_cleanup_max_loss = FloatProperty(name='Max weight removed (%)', description='Maximum total original influence removed from any vertex, including tiny weights. Export stops if cleanup needs a larger change. Higher values can change movement more', default=25, min=0, max=100, precision=1)
    bpy.types.Scene.mksm_cleanup_report = StringProperty()
    bpy.types.Scene.mksm_texture_count = IntProperty(name='Game textures', description='0: use all available slots as needed. Use 2 or 3 to combine images into fewer atlases. Slots used by unselected native meshes stay protected', default=0, min=0, max=64)
    bpy.types.Scene.mksm_template_glb = StringProperty(name='Destination Studio GLB', subtype='FILE_PATH')
    bpy.types.Scene.mksm_prepared_id = StringProperty()
    bpy.types.Scene.mksm_prepare_report = StringProperty()
    for cls in classes:
        if cls != MKSM_RetargetMap: bpy.utils.register_class(cls)
    bpy.types.Scene.mksm_animation_manifest = StringProperty(name='Animation source manifest', subtype='FILE_PATH')
    bpy.types.Scene.mksm_studio_exe = StringProperty(name='Studio application', subtype='FILE_PATH', description='MKSM Studio.exe compiles native PME2 and game texture data')
    bpy.types.Scene.mksm_native_source = StringProperty(name='Untouched game model (.original.pme2)', subtype='FILE_PATH', description='Choose the ORIGINAL Shaolin Monks .original.pme2 saved by Studio. Not your replacement GLB, BIN, or Blender file. Keep the matching textures companion beside it.')
def unregister():
    for name in ('mksm_source_rig','mksm_target_rig','mksm_bone_map','mksm_bone_map_index','mksm_map_source','mksm_map_target','mksm_retarget_fit','mksm_show_blend_map','mksm_retarget_report'):
        delattr(bpy.types.Scene,name)
    del bpy.types.Scene.mksm_reduction_triangles
    del bpy.types.Scene.mksm_reduction_deviation
    del bpy.types.Scene.mksm_reduction_weld
    del bpy.types.Scene.mksm_reduction_report
    del bpy.types.Scene.mksm_auto_cleanup
    del bpy.types.Scene.mksm_cleanup_max_loss
    del bpy.types.Scene.mksm_cleanup_report
    del bpy.types.Scene.mksm_texture_count
    del bpy.types.Scene.mksm_template_glb
    del bpy.types.Scene.mksm_prepared_id
    del bpy.types.Scene.mksm_prepare_report
    del bpy.types.Scene.mksm_animation_manifest
    del bpy.types.Scene.mksm_studio_exe
    del bpy.types.Scene.mksm_native_source
    for cls in reversed(classes):bpy.utils.unregister_class(cls)
if __name__=='__main__':register()


