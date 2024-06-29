import { Button, Card, CardContent } from "@mui/joy";
import Typography from "@mui/joy/Typography";
import * as React from "react";
import { useGoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { API_URL } from "../../constants";

function LoginPage({ setUser }) {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        paddingTop: "25vh",
      }}
    >
      <LoginCard setUser={setUser} />
    </div>
  );
}

function LoginCard({ setUser }) {
  const login = useGoogleLogin({
    onSuccess: (codeResponse) => {
      axios
        .post(API_URL + "/auth/code", {
          code: codeResponse["code"],
        })
        .then((res) => {
          setUser(res.data.info);
          console.log(res.data.info);
          sessionStorage.setItem("user", JSON.stringify(res.data.info));
          sessionStorage.setItem("id_token", res.data.id_token);
          console.log(res.data.id_token);
        })
        .catch((error) => {
          alert(error);
        });
    },
    scope: "openid email",
    flow: "auth-code",
  });
  return (
    <Card
      color="primary"
      orientation="vertical"
      size="lg"
      variant="outlined"
      sx={{
        alignItems: "center",
      }}
    >
      <Typography level="title-lg" textColor="text.primary">
        ERSMS Storage Login
      </Typography>
      <CardContent orientation="horizontal" sx={{ paddingTop: "32px" }}>
        <Button onClick={() => login()}>Sign in with Google 🚀</Button>
      </CardContent>
    </Card>
  );
}

export default LoginPage;
