{
  'includes' :['../../build/common.gypi'],
  'targets': [
    {
      'target_name': 'pinyin_input',
      'type': '<(library)',
      'include_dirs': [
        '<(SHARED_INTERMEDIATE_DIR)/protoc_out',
      ],
      'sources': [
        'pinyin_input_component.cc',
		'pinyin_input_component.h',
      ],
      'dependencies': [
        '<(DEPTH)/base/base.gyp:base',
        '<(DEPTH)/ipc/ipc.gyp:ipc',
        '<(DEPTH)/ipc/protos/protos.gyp:protos-cpp',
      ],
    },
  ]
}
