import React, { Component, createRef } from "react";

import "./chatContent.css";
import Avatar from "../chatList/Avatar";
import ChatItem from "./ChatItem";
import axios from "axios";

export default class ChatContent extends Component {
  studentImg =
    "https://cdn.pixabay.com/photo/2017/01/31/21/23/avatar-2027366_1280.png";
  botImg = "https://w3.sdu.edu.tr/assets/img/sdu-logo.png";

  messagesEndRef = createRef(null);
  chatItms = [
    {
      image: this.botImg,
      type: "other",
      msg: "Merhaba Size Nasıl Yardımcı Olabilirim?",
    },
  ];

  constructor(props) {
    super(props);
    this.state = {
      chat: this.chatItms,
      msg: "",
    };
  }
  onStateChange = (e) => {
    this.setState({ msg: e.target.value });
  };
  getAnswer(question) {
    return axios
      .post(`http://127.0.0.1:8000/department`, { question: question })
      .then((firm) => {
        return firm.data;
      });
  }
  handleMessageSubmit = async (e) => {
    const x = await this.getAnswer(this.state.msg);
    const newMessage = {
      image: this.studentImg,
      type: "",
      msg: this.state.msg,
    };
    const answer = {
      image: this.botImg,
      type: "other",
      msg: x.answer,
    };
    this.chatItms.push(newMessage);
    this.chatItms.push(answer);
    this.setState({ chat: this.chatItms });
    //setMessages([...messages, newMessage]);
    //messageInput.value = '';
  };
  render() {
    return (
      <div className="main__chatcontent">
        <div className="content__header">
          <div className="blocks">
            <div className="current-chatting-user">
              <Avatar isOnline="active" image={this.botImg} />
              <p>SDÜ Endüstri Mühendisliği</p>
            </div>
          </div>
        </div>
        <div className="content__body">
          <div className="chat__items">
            {this.state.chat.map((itm, index) => {
              return (
                <ChatItem
                  animationDelay={index + 2}
                  user={itm.type ? itm.type : "me"}
                  msg={itm.msg}
                  image={itm.image}
                />
              );
            })}
            <div ref={this.messagesEndRef} />
          </div>
        </div>
        <div className="content__footer">
          <div className="sendNewMessage">
            <input
              type="text"
              placeholder="Type a message here"
              onChange={this.onStateChange}
              value={this.state.msg}
            />
            <button
              onClick={this.handleMessageSubmit}
              className="btnSendMsg"
              id="sendMsgBtn"
            >
              <i className="fa fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </div>
    );
  }
}
