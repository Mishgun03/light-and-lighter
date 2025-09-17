import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Leaderboard() {
  const [rows, setRows] = useState([]);
  const [lbId, setLbId] = useState("EA6_SHR");
  useEffect(() => {
    fetchLb();
  }, [lbId]);

  async function fetchLb() {
    const { data } = await axios.get("/api/leaderboard/", {
      params: { id: lbId },
    });
    setRows(data.entries || []);
  }

  return (
    <div>
      <h3>Leaderboard</h3>
      <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
        <input value={lbId} onChange={(e) => setLbId(e.target.value)} />
        <button onClick={fetchLb}>Load</button>
      </div>
      <ol>
        {rows.map((r) => (
          <li key={r.character}>
            {r.current_position}. {r.character} — {r.class} — {r.score}
          </li>
        ))}
      </ol>
    </div>
  );
}
