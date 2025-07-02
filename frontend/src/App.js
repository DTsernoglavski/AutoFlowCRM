import React, { useState, useRef } from "react";

function App() {
  const [status, setStatus] = useState("");
  const signatureRef = useRef();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = {
      first_name: e.target.first_name.value,
      birth_date: e.target.birth_date.value,
      citizenship: e.target.citizenship.value,
      profession: e.target.profession.value,
      signature: signatureRef.current.toDataURL(),
    };
    setStatus("Sending...");
    const resp = await fetch("/api/documents/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (resp.ok) setStatus("Queued");
    else setStatus("Error");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="first_name" placeholder="First Name" required />
      <input name="birth_date" placeholder="Birth Date" required />
      <input name="citizenship" placeholder="Citizenship" required />
      <input name="profession" placeholder="Profession" required />
      <canvas ref={signatureRef} width={200} height={60} style={{ border: "1px solid #000" }} />
      <button type="submit">Send</button>
      <div>Status: {status}</div>
    </form>
  );
}

export default App;
