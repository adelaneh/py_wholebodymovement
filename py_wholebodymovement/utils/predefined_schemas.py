#!/usr/bin/env python
# coding: utf-8

_JOINT_NAMES_1 = [
	'Waist',
	'Torso',
	'Neck',
	'Head',
	'LeftShoulder',
	'LeftElbow',
	'LeftWrist',
	'LeftHand',
	'RightShoulder',
	'RightElbow',
	'RightWrist',
	'RightHand',
	'LeftHip',
	'LeftKnee',
	'LeftAnkle',
	'LeftFoot',
	'RightHip',
	'RightKnee',
	'RightAnkle',
	'RightFoot',
]

_ARTICULATED_FIGURE_ANGLES_1 = {
    'rshldr_theta': ("RightShoulder", "Neck", "RightElbow", 1, True), ## Right Shoulder
    'lshldr_theta': ("LeftShoulder", "Neck", "LeftElbow", -1, True), ## Left Shoulder
    'relbw_theta': ("RightElbow", "RightShoulder", "RightWrist", 1, True), ## Right Elbow
    'lelbw_theta': ("LeftElbow", "LeftShoulder", "LeftWrist", -1, True), ## Left Elbow
    'rwrst_theta': ("RightWrist", "RightElbow", "RightHand", 1, True), ## Right Wrist
    'lwrst_theta': ("LeftWrist", "LeftElbow", "LeftHand", -1, True), ## Left Wrist
    'rhip_theta': ("RightHip", "Waist", "RightKnee", 1, True), ## Right Hip
    'lhip_theta': ("LeftHip", "Waist", "LeftKnee", -1, True), ## Left Hip
    'rkn_theta': ("RightKnee", "RightHip", "RightAnkle", 1, True), ## Right Knee
    'lkn_theta': ("LeftKnee", "LeftHip", "LeftAnkle", -1, True), ## Left knee
    'rankl_theta': ("RightAnkle", "RightKnee", "RightFoot", 1, True), ## Right Ankle
    'lankl_theta': ("LeftAnkle", "LeftKnee", "LeftFoot", -1, True), ## Left Ankle
    'rnck_theta': ("Neck", "Head", "RightShoulder", 1, True), ## Neck/Right Shoulder
    'lnck_theta': ("Neck", "Head", "LeftShoulder", -1, True), ## Neck/Left Shoulder
    'rwst_theta': ("Waist", "Neck", "RightHip", 1, True), ## Waist/Right Hip
    'lwst_theta': ("Waist", "Neck", "LeftHip", -1, True), ## Waist/Left Hip
    'trso_theta': ("Torso", "Neck", "Waist", 1, True), ## Torso	
}

_JOINT_NAMES_2 = [
	'nose',
	'leye',
	'reye',
	'lear',
	'rear',
	'lshldr',
	'rshldr',
	'lelbw',
	'relbw',
	'lwrst',
	'rwrst',
	'lhip',
	'rhip',
	'lkn',
	'rkn',
	'lankl',
	'rankl'
]

_EXTENDED_JOINT_NAMES_2 = {
    'neck': ('lshldr', 'rshldr', 'lshldr', 'rshldr'), ## Neck
    'torso': ('lhip', 'rhip', 'lhip', 'rhip'), ## Torso
    'vaxis': ('lhip', 'rhip', 'lshldr', 'rshldr'), ## Vertical Axis
}

_ARTICULATED_FIGURE_ANGLES_2 = {
    'rswt_theta': ("neck", "rwrst", "torso", -1, True), ## Right Wrist->Neck->Torso
    'lswt_theta': ("neck", "lwrst", "torso",  1, True), ## Left Wrist->Neck->Torso
    'rahn_theta': ("rhip", "rankl", "nose", -1, True), ## Right Ankle->Hip->Nose
    'lahn_theta': ("lhip", "lankl", "nose",  1, True), ## Left Ankle->Hip->Nose
    'ratk_theta': ("torso", "rankl", "neck", -1, True), ## Right Ankle->Torso->Neck
    'latk_theta': ("torso", "lankl", "neck",  1, True), ## Left Ankle->Torso->Neck
    'tkf_theta': ("torso", "vaxis", "neck", 1, False), ## Neck->Torso->VerticalAxis (Backbone)
}


_JOINT_NAMES_3 = [
    'Head',
    'Neck',
    'SpineB',        # Spine base - pelvis (waist)
    'SpineM',        # Spine mid - mid point (torso)
    'SpineSh',       # Spine shoulder - spine point in between the clavicles
    'LeftShoulder',
    'LeftElbow',
    'LeftWrist',
    'LeftHand',
    'RightShoulder',
    'RightElbow',
    'RightWrist',
    'RightHand',
    'LeftHip',
    'LeftKnee',
    'LeftAnkle',
    'LeftFoot',
    'RightHip',
    'RightKnee',
    'RightAnkle',
    'RightFoot',
]

_ARTICULATED_FIGURE_ANGLES_3 = {
    'rshldr_theta': ("RightShoulder", "Neck", "RightElbow", 1, True), ## Right Shoulder
    'lshldr_theta': ("LeftShoulder", "Neck", "LeftElbow", -1, True), ## Left Shoulder
    'relbw_theta': ("RightElbow", "RightShoulder", "RightWrist", 1, True), ## Right Elbow
    'lelbw_theta': ("LeftElbow", "LeftShoulder", "LeftWrist", -1, True), ## Left Elbow
    'rwrst_theta': ("RightWrist", "RightElbow", "RightHand", 1, True), ## Right Wrist
    'lwrst_theta': ("LeftWrist", "LeftElbow", "LeftHand", -1, True), ## Left Wrist
    'rhip_theta': ("RightHip", "SpineB", "RightKnee", 1, True), ## Right Hip
    'lhip_theta': ("LeftHip", "SpineB", "LeftKnee", -1, True), ## Left Hip
    'rkn_theta': ("RightKnee", "RightHip", "RightAnkle", 1, True), ## Right Knee
    'lkn_theta': ("LeftKnee", "LeftHip", "LeftAnkle", -1, True), ## Left knee
    'rankl_theta': ("RightAnkle", "RightKnee", "RightFoot", 1, True), ## Right Ankle
    'lankl_theta': ("LeftAnkle", "LeftKnee", "LeftFoot", -1, True), ## Left Ankle
    'rnck_theta': ("Neck", "Head", "RightShoulder", 1, True), ## Neck/Right Shoulder
    'lnck_theta': ("Neck", "Head", "LeftShoulder", -1, True), ## Neck/Left Shoulder
    'rwst_theta': ("SpineB", "Neck", "RightHip", 1, True), ## SpineB/Right Hip
    'lwst_theta': ("SpineB", "Neck", "LeftHip", -1, True), ## SpineB/Left Hip
    'trso_theta': ("SpineM", "Neck", "SpineB", 1, True), ## SpineM	
}

