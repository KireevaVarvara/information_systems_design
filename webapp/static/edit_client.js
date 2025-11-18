const form = document.getElementById("client-form");
const messageBox = document.getElementById("message");
const submitBtn = form.querySelector("button[type='submit']");
const title = document.getElementById("title");

const showMessage = (text, isError = false) => {
  messageBox.textContent = text;
  messageBox.classList.toggle("error", isError);
  messageBox.classList.remove("hidden");
};

const hideMessage = () => {
  messageBox.classList.add("hidden");
};

const fillForm = (client) => {
  const set = (name, value) => {
    const input = form.querySelector(`[name='${name}']`);
    if (input) {
      input.value = value ?? "";
    }
  };
  title.textContent = `${client.surname} ${client.firstname}`;
  set("surname", client.surname);
  set("firstname", client.firstname);
  set("fathers_name", client.fathers_name);
  set("birth_date", client.birth_date);
  set("phone_number", client.phone_number);
  set("pasport", client.pasport);
  set("email", client.email);
  set("balance", client.balance);
};

const serialize = (formData) => {
  const payload = {};
  formData.forEach((value, key) => {
    const trimmed = value.trim();
    if (trimmed === "") {
      payload[key] = null;
      return;
    }
    if (key === "balance") {
      payload[key] = Number(trimmed);
      return;
    }
    payload[key] = trimmed;
  });
  return payload;
};

const validateRequired = (payload) => {
  const required = ["surname", "firstname", "birth_date"];
  const missing = required.filter((field) => !payload[field]);
  if (missing.length) {
    throw new Error("Заполните обязательные поля: фамилия, имя, дата рождения.");
  }
};

const loadClient = async (clientId) => {
  try {
    const response = await fetch(`/api/clients/${clientId}`);
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || "Не удалось загрузить клиента");
    }
    const client = await response.json();
    fillForm(client);
  } catch (error) {
    showMessage(error.message, true);
  }
};

const handleSuccess = () => {
  showMessage("Клиент обновлен. Окно закроется...", false);
  if (window.opener) {
    window.opener.postMessage("client-updated", "*");
  }
  setTimeout(() => window.close(), 800);
};

const handleSubmit = async (event) => {
  event.preventDefault();
  hideMessage();
  submitBtn.disabled = true;

  const params = new URLSearchParams(window.location.search);
  const clientId = params.get("id");
  if (!clientId) {
    showMessage("Не указан ID клиента", true);
    submitBtn.disabled = false;
    return;
  }

  const payload = serialize(new FormData(form));

  try {
    validateRequired(payload);
    const response = await fetch(`/api/clients/${clientId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Не удалось обновить клиента");
    }
    handleSuccess();
  } catch (error) {
    showMessage(error.message, true);
  } finally {
    submitBtn.disabled = false;
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const clientId = params.get("id");
  if (!clientId) {
    showMessage("Не указан ID клиента", true);
    return;
  }
  loadClient(clientId);
});

form.addEventListener("submit", handleSubmit);
