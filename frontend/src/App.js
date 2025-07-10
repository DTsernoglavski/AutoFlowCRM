import SignatureCanvas from 'react-signature-canvas';
import { useState, useRef } from 'react';
import './App.css';

function App() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    gender: '',
    phone: '',
    employmentType: '',
    role: '',
    startDate: '',
    salary: '',
    distributionRatio: ''
  });
  const [errors, setErrors] = useState({});
  const sigCanvas = useRef({});

  const validate = () => {
    const errors = {};
    const latinRegex = /^[A-Za-z\s]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[0-9+\s()-]{7,}$/;
    const salaryRegex = /^\d+(\.\d{1,2})?$/;
    const ratioRegex = /^\d+$/;

    if (!latinRegex.test(form.username.trim())) {
      errors.username = 'Имя должно быть только латиницей';
    }

    if (!emailRegex.test(form.email.trim())) {
      errors.email = 'Некорректный email';
    }

    if (!form.gender) {
      errors.gender = 'Выберите пол';
    }

    if (!phoneRegex.test(form.phone.trim())) {
      errors.phone = 'Введите корректный номер телефона';
    }

    if (!form.employmentType) {
      errors.employmentType = 'Укажите тип занятости';
    }

    if (!form.role.trim()) {
      errors.role = 'Укажите роль';
    }

    if (!form.startDate) {
      errors.startDate = 'Выберите дату начала';
    }

    if (!salaryRegex.test(form.salary.trim())) {
      errors.salary = 'Введите зарплату в формате: 12345.67';
    }

    if (!ratioRegex.test(form.distributionRatio.trim())) {
      errors.distributionRatio = 'Введите целое число для Fördelningstal';
    }

    return errors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) return;

    const data = {
      ...form,
      signature: sigCanvas.current.getTrimmedCanvas().toDataURL()
    };

    try {
      await fetch('/api/documents/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      alert('Форма успешно отправлена!');
    } catch (err) {
      console.error(err);
      alert('Ошибка при отправке');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <label>
        Имя:
        <input name="username" value={form.username} onChange={handleChange} />
        {errors.username && <span className="error">{errors.username}</span>}
      </label>

      <label>
        Email:
        <input name="email" value={form.email} onChange={handleChange} />
        {errors.email && <span className="error">{errors.email}</span>}
      </label>

      <label>
        Пол:
        <select name="gender" value={form.gender} onChange={handleChange}>
          <option value="">Выберите</option>
          <option value="male">Мужской</option>
          <option value="female">Женский</option>
        </select>
        {errors.gender && <span className="error">{errors.gender}</span>}
      </label>

      <label>
        Телефон:
        <input
          name="phone"
          inputMode="tel"
          value={form.phone}
          onChange={handleChange}
          placeholder="+372 512 3456"
        />
        {errors.phone && <span className="error">{errors.phone}</span>}
      </label>

      <label>
        Тип занятости:
        <select name="employmentType" value={form.employmentType} onChange={handleChange}>
          <option value="">Выберите</option>
          <option value="Permanent">Постоянный</option>
          <option value="Temporary">Временный</option>
          <option value="Freelance">Фриланс</option>
        </select>
        {errors.employmentType && <span className="error">{errors.employmentType}</span>}
      </label>

      <label>
        Роль по контракту:
        <input name="role" value={form.role} onChange={handleChange} />
        {errors.role && <span className="error">{errors.role}</span>}
      </label>

      <label>
        Дата начала:
        <input name="startDate" type="date" value={form.startDate} onChange={handleChange} />
        {errors.startDate && <span className="error">{errors.startDate}</span>}
      </label>

      <label>
        Зарплата (до налога):
        <input name="salary" value={form.salary} onChange={handleChange} placeholder="Пример: 25000.00" />
        {errors.salary && <span className="error">{errors.salary}</span>}
      </label>

      <label>
        Fördelningstal:
        <input name="distributionRatio" value={form.distributionRatio} onChange={handleChange} />
        {errors.distributionRatio && <span className="error">{errors.distributionRatio}</span>}
      </label>

      <label>Подпись:</label>
      <SignatureCanvas
        ref={sigCanvas}
        canvasProps={{ width: 400, height: 150, className: 'sigCanvas' }}
      />

      <button type="submit">Generate User Key</button>
    </form>
  );
}

export default App;