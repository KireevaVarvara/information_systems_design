const form = document.getElementById("client-form");
const messageBox = document.getElementById("message");
const submitBtn = form.querySelector("button[type='submit']");

const showMessage = (text, isError = false) => {
  messageBox.textContent = text;
  messageBox.classList.toggle("error", isError);
  messageBox.classList.remove("hidden");
};

const hideMessage = () => {
  messageBox.classList.add("hidden");
};

const serialize = (formData) => {
  const payload = {};
  formData.forEach((value, key) => {
    const trimmed = value.trim();
    if (trimmed === "") {
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

const handleSuccess = () => {
  showMessage("Клиент создан. Окно закроется...", false);
  if (window.opener) {
    window.opener.postMessage("client-added", "*");
  }
  setTimeout(() => window.close(), 800);
};

const handleSubmit = async (event) => {
  event.preventDefault();
  hideMessage();
  submitBtn.disabled = true;

  const payload = serialize(new FormData(form));

  try {
    validateRequired(payload);
    const response = await fetch("/api/clients", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Не удалось создать клиента");
    }

    handleSuccess();
  } catch (error) {
    showMessage(error.message, true);
  } finally {
    submitBtn.disabled = false;
  }
};

form.addEventListener("submit", handleSubmit);
