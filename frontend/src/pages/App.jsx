import React, { useEffect, useState } from "react";
import { Link, Outlet, useNavigate } from "react-router-dom";
import { clearToken, getToken } from "../auth";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Stack,
} from "@mui/material";
import { useQueryClient } from "@tanstack/react-query";

export default function App() {
  const [auth, setAuth] = useState(!!getToken());
  useEffect(() => {
    setAuth(!!getToken());
  });
  const navigate = useNavigate();

  const queryClient = useQueryClient();

  return (
    <>
      <AppBar
        position="sticky"
        color="transparent"
        elevation={0}
        sx={{ borderBottom: "1px solid rgba(255,255,255,0.08)" }}
      >
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            DarkerDB
          </Typography>
          <Stack gap="8px" direction="row" alignItems="center">
            <Button color="inherit" component={Link} to="/">
              Dashboard
            </Button>
            <Button color="inherit" component={Link} to="/items">
              Items
            </Button>
            <Button color="inherit" component={Link} to="/leaderboard">
              Leaderboard
            </Button>
            {!auth && (
              <Button color="inherit" component={Link} to="/login">
                Login
              </Button>
            )}
            {!auth && (
              <Button color="inherit" component={Link} to="/register">
                Register
              </Button>
            )}
            {auth && (
              <Button
                color="inherit"
                onClick={() => {
                  clearToken();
                  queryClient.clear();
                  queryClient.invalidateQueries();
                  navigate("/items");
                }}
              >
                Logout
              </Button>
            )}
          </Stack>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 3 }}>
        <Outlet />
      </Container>
    </>
  );
}
