import React, { Component } from "react";
import "./userProfile.css";

export default class UserProfile extends Component {
  toggleInfo = (e) => {
    e.target.parentNode.classList.toggle("open");
  };
  render() {
    return (
      <div className="main__userprofile">
        <div className="profile__card user__profile__image">
          <div className="profile__image">
            <img src="https://cdn.pixabay.com/photo/2017/01/31/21/23/avatar-2027366_1280.png" />
          </div>
          <h4>Öğrenci</h4>
          <p>Endüstri Mühendisi Adayı</p>
        </div>
      </div>
    );
  }
}
