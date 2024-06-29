import * as React from "react";
import { useEffect, useState } from "react";
import MainPage from "./components/MainPage";
import LoginPage from "./components/Login/LoginPage";
import { Dialog } from "@mui/material";
import { DialogTitle } from "@mui/joy";
import ShareForm from "./components/ShareForm";
import SimpleSnackbar from "./components/NotificationSnackbar";

export default function EteamApp() {
  const [user, setUser] = useState<any | null>(null);
  const [open, setOpen] = React.useState(false);

  useEffect(() => {
    try {
      const user = JSON.parse(sessionStorage.user);
      setUser(user);
    } catch (error) {}
  }, []);
  return (
    <div>
      {user != null ? (
        <MainPage setDialog={setOpen} user={user} setUser={setUser} />
      ) : (
        <div>
          <LoginPage setUser={setUser} />
        </div>
      )}
      <ShareForm open={open} setOpen={setOpen}></ShareForm>
      <SimpleSnackbar></SimpleSnackbar>
    </div>
  );
}
