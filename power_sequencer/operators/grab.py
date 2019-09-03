#
# Copyright (C) 2016-2019 by Nathan Lovato, Daniel Oakey, Razvan Radulescu, and contributors
#
# This file is part of Power Sequencer.
#
# Power Sequencer is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Power Sequencer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Power Sequencer. If
# not, see <https://www.gnu.org/licenses/>.
#
import bpy

from .utils.functions import get_mouse_frame_and_channel
from .utils.global_settings import SequenceTypes
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class POWER_SEQUENCER_OT_grab(bpy.types.Operator):
    """
    *brief* Grab and move sequences. Extends Blender's built-in grab tool


    Grab and move sequences. If you have no strips selected, it automatically
    finds the strip closest to the mouse and selects it. If you only select
    one or multiple crossfades, selects the handles on either side of the
    crossfades before moving sequences, using POWER_SEQUENCER_OT_crossfade_edit
    """

    doc = {
        "name": doc_name(__qualname__),
        "demo": "",
        "description": doc_description(__doc__),
        "shortcuts": [({"type": "G", "value": "PRESS"}, {}, "")],
        "keymap": "Sequencer",
    }
    bl_idname = doc_idname(__qualname__)
    bl_label = doc["name"]
    bl_description = doc_brief(doc["description"])
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        frame, channel = get_mouse_frame_and_channel(context, event)
        if not context.selected_sequences:
            bpy.ops.power_sequencer.select_closest_to_mouse(frame=frame, channel=channel)
        return self.execute(context)

    def execute(self, context):
        if len(context.selected_sequences) == 0:
            return {'FINISHED'}

        strip = context.selected_sequences[0]
        if len(context.selected_sequences) == 1 and strip.type in SequenceTypes.TRANSITION:
            context.scene.sequence_editor.active_strip = strip
            return bpy.ops.power_sequencer.crossfade_edit()
        else:
            return bpy.ops.transform.seq_slide('INVOKE_DEFAULT')
