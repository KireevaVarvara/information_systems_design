const messageBox = document.getElementById("message");
const detailsContainer = document.getElementById("client-details");
const title = document.getElementById("client-name");

const showMessage = (text, isError = false) => {
  messageBox.textContent = text;
  messageBox.classList.toggle("error", isError);
  messageBox.classList.remove("hidden");
};

const hideMessage = () => {
  messageBox.classList.add("hidden");
};

const renderDetails = (client) => {
  title.textContent = `${client.surname} ${client.firstname}`;
  const rows = [
    ["ID", client.id],
    ["Фамилия", client.surname],
    ["Имя", client.firstname],
    ["Отчество", client.fathers_name || "—"],
    ["Дата рождения", client.birth_date || "—"],
    ["Телефон", client.phone_number || "—"],
    ["Паспорт", client.pasport || "—"],
    ["Email", client.email || "—"],
    ["Баланс", client.balance ?? "—"],
  ];

  rows.forEach(([label, value]) => {
    const dt = document.createElement("dt");
    dt.textContent = label;
    const dd = document.createElement("dd");
    dd.textContent = value;
    detailsContainer.appendChild(dt);
    detailsContainer.appendChild(dd);
  });
};

const loadClient = async () => {
  hideMessage();
  const params = new URLSearchParams(window.location.search);
  const clientId = params.get("id");

  if (!clientId) {
    showMessage("Не передан идентификатор клиента", true);
    return;
  }

  try {
    const response = await fetch(`/api/clients/${clientId}`);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Не удалось загрузить данные клиента");
    }

    const client = await response.json();
    renderDetails(client);
  } catch (error) {
    showMessage(error.message, true);
  }
};

document.addEventListener("DOMContentLoaded", loadClient);
