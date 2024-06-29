// @ts-ignore
import React from "react";
// @ts-ignore
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App.js";
import { GoogleOAuthProvider } from "@react-oauth/google";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <GoogleOAuthProvider clientId="956347756063-vf9v5mvgcpr7jdcj64gm6572tsqmn9v2.apps.googleusercontent.com">
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </GoogleOAuthProvider>,
);
