/*
  Copyright 2014 Google Inc.

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
*/

#include "components/pinyin_input/pinyin_input_component.h"

#include <string>

#include "base/logging.h"
#include "base/scoped_ptr.h"
#include "base/stl_util.h"
#include "components/common/constants.h"
#include "components/common/file_utils.h"
#include "components/common/keystroke_util.h"
#include "ipc/constants.h"
#include "ipc/message_types.h"
#include "ipc/protos/ipc.pb.h"
#include "ipc/message_util.h"
namespace {

// The message types keyboard input ime can consume.
const uint32 kConsumeMessages[] = {
  // Input context related messages.
  ipc::MSG_ATTACH_TO_INPUT_CONTEXT,
  ipc::MSG_PROCESS_KEY_EVENT,
  // Composition related messages.
  ipc::MSG_CANCEL_COMPOSITION,
  ipc::MSG_COMPLETE_COMPOSITION,
  ipc::MSG_QUERY_CANDIDATE_LIST,
  ipc::MSG_QUERY_COMPOSITION
};

const uint32 kProduceMessages[] = {
  ipc::MSG_REQUEST_CONSUMER,
  ipc::MSG_SET_COMPOSITION,
  ipc::MSG_INSERT_TEXT,
};

static const char kPinyinImeLanguage[] = "cn";
static const char kPinyinImeIcon[]  = "cn.png";
static const char kPinyinImeOverIcon[]  = "cn_over.png";
static const char kResourcePackPathPattern[] = "/pinyin_input_[LANG].pak";
}  // namespace
namespace ime_goopy {
namespace components {

using ipc::proto::Message;


PinyinInputComponent::PinyinInputComponent() {
}

PinyinInputComponent::~PinyinInputComponent() {
}

void PinyinInputComponent::GetInfo(ipc::proto::ComponentInfo* info) {
  info->set_string_id(kPinyinInputComponentStringId);
  info->add_language(kPinyinImeLanguage);
  for (int i = 0; i < arraysize(kConsumeMessages); ++i)
    info->add_consume_message(kConsumeMessages[i]);
  for (int i = 0; i < arraysize(kProduceMessages); ++i)
    info->add_produce_message(kProduceMessages[i]);
  GetSubComponentsInfo(info);
  std::string dir = FileUtils::GetDataPathForComponent(
      kPinyinInputComponentStringId);
  std::string filename = dir + "/" + kPinyinImeOverIcon;
  ipc::proto::IconGroup icon;
  if (!FileUtils::ReadFileContent(filename,
                                  icon.mutable_over()->mutable_data())) {
    icon.clear_over();
  }
  filename = dir + "/" + kPinyinImeIcon;
  if (FileUtils::ReadFileContent(filename,
                                 icon.mutable_normal()->mutable_data())) {
    info->mutable_icon()->CopyFrom(icon);
  }
  std::string name = "CN";
  info->set_name(name.c_str());
}

void PinyinInputComponent::Handle(Message* message) {
  DCHECK(id());
  // This message is consumed by sub components.
  if (HandleMessageBySubComponents(message))
    return;
  scoped_ptr<Message> mptr(message);

  switch (mptr->type()) {
    case ipc::MSG_ATTACH_TO_INPUT_CONTEXT:
      OnMsgAttachToInputContext(mptr.release());
      break;
    case ipc::MSG_PROCESS_KEY_EVENT:
      OnMsgProcessKey(mptr.release());
      break;
    case ipc::MSG_CANCEL_COMPOSITION:
      // ReplyTrue in case the source component uses SendWithReply.
      ReplyTrue(mptr.release());
      break;
    case ipc::MSG_COMPLETE_COMPOSITION:
      ReplyTrue(mptr.release());
      break;
	case ipc::MSG_QUERY_CANDIDATE_LIST:
		OnMsgQueryCandidateList(mptr.release());
	  break;
	case ipc::MSG_QUERY_COMPOSITION:
		OnMsgQueryComposition(mptr.release());
		break;
    default: {
      DLOG(ERROR) << "Unexpected message received:"
                  << "type = " << mptr->type()
                  << "icid = " << mptr->icid();
      ReplyError(mptr.release(), ipc::proto::Error::INVALID_MESSAGE,
                 "unknown type");
      break;
    }
  }
}

void PinyinInputComponent::OnMsgAttachToInputContext(Message* message) {
	
	scoped_ptr<Message> mptr(message);
	uint32 icid = mptr->icid();
  //DCHECK_EQ(mptr->reply_mode(), Message::NEED_REPLY);
  ReplyTrue(mptr.release());
  /*
  scoped_ptr<ipc::proto::Message> mptr(NewMessage(
	  ipc::MSG_QUERY_COMPONENT,
	  message->icid(),
	  true));
  Message* query_msg  = NewMessage(ipc::MSG_QUERY_COMPONENT, message->icid(), true);
  */

  if (icid != ipc::kInputContextNone) {
	  message = NewMessage(ipc::MSG_REQUEST_CONSUMER, icid, false);

	  // Although we only produce broadcast messages, we still need at least one
	  // component to handle them to show the composition text and candidate list
	  // to the user.
	  for (size_t i = 0; i < arraysize(kProduceMessages); ++i)
		  message->mutable_payload()->add_uint32(kProduceMessages[i]);
	  uint32 serial;
	  Send(message, &serial);
	  
  }

 }

void PinyinInputComponent::OnMsgProcessKey(Message* message) {
	scoped_ptr<Message> mptr(message);
	
	//only process down
	if (mptr->has_payload() && mptr->payload().has_key_event()) {
		
		if (mptr->payload().key_event().type() == 1) {
			ReplyTrue(mptr.release());
			return;
		}
	}
	_composition = _composition + mptr->payload().key_event().text();
	ReplyTrue(mptr.release());
	
	Message* insert_msg = NewMessage(ipc::MSG_SET_COMPOSITION, message->icid(), true);
	string text = "*";
	insert_msg->mutable_payload()->mutable_composition()->mutable_text()->set_text(_composition); //= string();
	//uint32 serial;
	ipc::proto::Message* reply = NULL;
	SendWithReply(insert_msg, -1, &reply);
	if(reply)
		delete reply;
	//
}

void PinyinInputComponent::OnMsgQueryCandidateList(ipc::proto::Message* message) {
	ipc::ConvertToReplyMessage(message);
	ipc::proto::CandidateList* candidate_list = message->mutable_payload()->mutable_candidate_list();
	ipc::proto::Candidate* candidate = candidate_list->add_candidate();
	candidate->mutable_text()->set_text("z");
	ipc::proto::Message* reply = NULL;
	SendWithReply(message, -1, &reply);
	if (reply)
		delete reply;
}
void  PinyinInputComponent::OnMsgQueryComposition(ipc::proto::Message* message) {
	ipc::ConvertToReplyMessage(message);
	ipc::proto::Composition*  composition = message->mutable_payload()->mutable_composition();
	composition->mutable_text()->set_text("z");
	//candidate->mutable_text()->set_text("z");
	ipc::proto::Message* reply = NULL;
	SendWithReply(message, -1, &reply);
	if (reply)
		delete reply;
}


}  // namespace components
}  // namespace ime_goopy
