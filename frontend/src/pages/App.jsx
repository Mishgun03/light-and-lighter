import React from 'react'
import { Link, Outlet } from 'react-router-dom'
import { clearToken, getToken } from '../auth'
import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material'

export default function App() {
  return (
    <>
      <AppBar position="sticky" color="transparent" elevation={0} sx={{ borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>DarkerDB</Typography>
          <Button color="inherit" component={Link} to="/">Dashboard</Button>
          <Button color="inherit" component={Link} to="/items">Items</Button>
          <Button color="inherit" component={Link} to="/leaderboard">Leaderboard</Button>
          {!getToken() && <Button color="inherit" component={Link} to="/login">Login</Button>}
          {!getToken() && <Button color="inherit" component={Link} to="/register">Register</Button>}
          {!!getToken() && <Button color="inherit" onClick={() => { clearToken(); location.href = '/' }}>Logout</Button>}
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ py: 3 }}>
        <Outlet />
      </Container>
    </>
  )
}


