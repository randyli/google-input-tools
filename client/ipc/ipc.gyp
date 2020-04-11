{
  'includes' :['../build/common.gypi'],
  'variables': {
    'srcs': [
      'channel_connector.h',
      'component.h',
      'component_base.cc',
      'component_base.h',
      'component_host.h',
      'constants.h',
      'default_input_method.cc',
      'default_input_method.h',
      'direct_message_channel.cc',
      'direct_message_channel.h',
      'hub.h',
      'hub_command_list_manager.cc',
      'hub_command_list_manager.h',
      'hub_component.cc',
      'hub_component.h',
      'hub_composition_manager.cc',
      'hub_composition_manager.h',
      'hub_host.cc',
      'hub_host.h',
      'hub_hotkey_list.cc',
      'hub_hotkey_list.h',
      'hub_hotkey_manager.cc',
      'hub_hotkey_manager.h',
      'hub_impl.cc',
      'hub_impl.h',
      'hub_input_context.cc',
      'hub_input_context.h',
      'hub_input_context_manager.cc',
      'hub_input_context_manager.h',
      'hub_input_method_manager.cc',
      'hub_input_method_manager.h',
      'hub_scoped_message_cache.cc',
      'message_channel_client_win.cc',
      'message_channel_server_win.cc',
      'message_channel_win.cc',
      'message_channel_win_consts.cc',
      'message_queue_win.cc',
      'message_queue.h',
      'message_types.cc',
      'message_types.h',
      'message_types_decl.h',
      'message_util.cc',
      'message_util.h',
      'multi_component_host.cc',
      'multi_component_host.h',
      'pipe_server_win.cc',
      'settings_client.cc',
      'settings_client.h',
      'simple_message_queue.cc',
      'simple_message_queue.h',
      'sub_component.h',
      'sub_component_base.cc',
      'sub_component_base.h',
      'testing.h',
      'testing_prod.h',
      'thread_message_queue_runner.cc',
      'thread_message_queue_runner.h',
    ],
  },
  'targets': [
    {
      'target_name': 'ipc',
      'type': '<(library)',
      'dependencies': [
        '<(DEPTH)/ipc/protos/protos.gyp:protos-cpp',
        '<(DEPTH)/base/base.gyp:base',
        '<(DEPTH)/third_party/protobuf/protobuf.gyp:protobuf',
      ],
      'include_dirs': [
        '<(SHARED_INTERMEDIATE_DIR)/protoc_out'
      ],
      'sources': [
        '<@(srcs)',
      ],
    },
    {
      'target_name': 'ipc_test_util',
      'type': '<(library)',
      'dependencies': [
        'ipc',
        'protos/protos.gyp:protos-cpp',
        '<(DEPTH)/third_party/gtest/gtest.gyp:gtest',
      ],
      'sources': [
        'hub_impl_test_base.cc',
        'hub_impl_test_base.h',
        'mock_component.cc',
        'mock_component.h',
        'mock_component_host.cc',
        'mock_component_host.h',
        'mock_connector.cc',
        'mock_connector.h',
        'mock_message_channel.cc',
        'mock_message_channel.h',
        'mock_message_channel_test.cc',
        'test_util.cc',
        'test_util.h',
      ],
    },
    {
      'target_name': 'ipc_unittests',
      'type': 'executable',
      'dependencies': [
        'ipc',
        'ipc_test_util',
        'protos/protos.gyp:protos-cpp',
        '<(DEPTH)/third_party/gtest/gtest.gyp:gtest',
      ],
      'sources': [
        'direct_message_channel_test.cc',
        'hub_command_list_manager_test.cc',
        'hub_component_test.cc',
        'hub_composition_manager_test.cc',
        'hub_host_test.cc',
        'hub_impl_test.cc',
        'hub_input_context_manager_test.cc',
        'hub_input_context_test.cc',
        'integration_test.cc',
        'message_types_test.cc',
        'mock_component_host_test.cc',
        'mock_message_channel_test.cc',
        'multi_component_host_test.cc',
        'settings_client_test.cc',
        'thread_message_queue_runner_test.cc',
        'unit_tests.cc',
      ],
    },
  ],
  'conditions': [
    ['OS=="win"', {
      'targets': [
        {
          'target_name': 'ipc_x64',
          'type': '<(library)',
          'dependencies': [
            '<(DEPTH)/ipc/protos/protos.gyp:protos-cpp_x64',
            '<(DEPTH)/base/base.gyp:base_x64',
            '<(DEPTH)/third_party/protobuf/protobuf.gyp:protobuf_x64',
          ],
          'include_dirs': [
            '<(SHARED_INTERMEDIATE_DIR)/protoc_out'
          ],
          'sources': [
            '<@(srcs)',
          ],
        },
      ],
    },],
  ],
}
