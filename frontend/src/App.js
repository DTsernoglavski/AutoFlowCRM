import { useRef, useState } from 'react';
import SignatureCanvas from 'react-signature-canvas';
import './App.css';

function App() {
  const [form, setForm] = useState({
    first_name: '',
    birth_date: '',
    citizenship: '',
    profession: ''
  });
  const sigRef = useRef();

  const handleChange = e =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    const signature = sigRef.current.isEmpty()
      ? ''
      : sigRef.current.getTrimmedCanvas().toDataURL();
    const res = await fetch(
      `${process.env.REACT_APP_API_URL}/api/documents/render`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, signature })
      }
    );
    const data = await res.json();
    alert(data.status === 'ok'
      ? 'Сгенерирован ' + data.path
      : 'Ошибка: ' + JSON.stringify(data));
  };

  return (
    <div className="App" style={{ padding: 20, maxWidth: 400, margin: 'auto' }}>
      <h2>Генерация документов</h2>
      <form onSubmit={handleSubmit}>
        <label>Имя (латиницей):<br/>
          <input name="first_name" value={form.first_name}
            onChange={handleChange} required/>
        </label><br/><br/>
        <label>Дата (YYYY-MM-DD):<br/>
          <input name="birth_date" value={form.birth_date}
            onChange={handleChange} required/>
        </label><br/><br/>
        <label>Гражданство:<br/>
          <input name="citizenship" value={form.citizenship}
            onChange={handleChange} required/>
        </label><br/><br/>
        <label>Профессия:<br/>
          <input name="profession" value={form.profession}
            onChange={handleChange} required/>
        </label><br/><br/>
        <label>Подпись:<br/>
          <SignatureCanvas ref={sigRef}
            penColor="black"
            canvasProps={{width:300, height:100, className:'sig-canvas'}}
          />
        </label><br/><br/>
        <button type="submit">Сгенерировать</button>
      </form>
    </div>
  );
}

export default App;
