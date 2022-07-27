import React from "react";
import "./Button.css";

const Menu = () => {
  return (
    <div className="button">
        <div>
            <label> Color </label>
            <input type="color"/>
        </div>
        <div>
            <button >undo</button>
            <button >redo</button>
        </div>
    </div>
  );
};

export default Menu;