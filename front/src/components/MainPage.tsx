import { CssVarsProvider } from "@mui/joy/styles";
import CssBaseline from "@mui/joy/CssBaseline";
import Layout from "./Layout";
import Header from "./Header";
import Navigation from "./Navigation";
import Box from "@mui/joy/Box";
import * as React from "react";
import MainContent from "./MainContent";
import { useState } from "react";
import PlanModal from "./PlanModal";

function MainPage({ setDialog, user, setUser }) {
  const [tab, setTab] = useState<string>("files");
  const [openDialog, setOpenDialog] = useState(false);

  return (
    <div>
      <PlanModal
        open={openDialog}
        onClose={() => {
          setOpenDialog(false);
        }}
        onClickSettings={() => {
          setTab("settings");
        }}
      ></PlanModal>
      <CssVarsProvider disableTransitionOnChange>
        <CssBaseline />
        <Layout.Root sx={{}}>
          <Layout.Header>
            <Header
              user={user}
              onLogout={() => {
                sessionStorage.removeItem("user");
                sessionStorage.removeItem("id_token");
                setUser(null);
              }}
              onClickSettings={() => setTab("settings")}
            />
          </Layout.Header>
          <Layout.SideNav>
            <Navigation tab={tab} setTab={setTab} />
          </Layout.SideNav>
          <Layout.Main>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                flexDirection: "column",
              }}
            >
              <MainContent
                tab={tab}
                setDialog={setDialog}
                openDialog={() => setOpenDialog(true)}
              />
            </Box>
          </Layout.Main>
        </Layout.Root>
      </CssVarsProvider>
    </div>
  );
}
export default MainPage;
