import React, { useState } from 'react'
import axios from 'axios'

export default function ResetPassword() {
  const [email, setEmail] = useState('')
  const [ok, setOk] = useState(false)
  async function submit(e) {
    e.preventDefault()
    await axios.post('/api/auth/password-reset/', { email }).catch(() => {})
    setOk(true)
  }
  return (
    <form onSubmit={submit} style={{ display: 'grid', gap: 8, maxWidth: 360 }}>
      <h3>Password Reset</h3>
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      {ok && <div>Instructions sent (check server logs in this demo).</div>}
      <button type="submit">Send</button>
    </form>
  )
}


