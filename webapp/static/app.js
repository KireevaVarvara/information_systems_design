const messageBox = document.getElementById("message");
const tableBody = document.querySelector("#clients-table tbody");
const createBtn = document.getElementById("create-btn");

const showMessage = (text, isError = false) => {
  messageBox.textContent = text;
  messageBox.classList.toggle("error", isError);
  messageBox.classList.remove("hidden");
};

const hideMessage = () => {
  messageBox.classList.add("hidden");
};

const openDetails = (id) => {
  window.open(`client.html?id=${id}`, "_blank", "noopener");
};

const openEdit = (id) => {
  window.open(`edit_client.html?id=${id}`, "_blank", "width=600,height=700");
};

const renderRow = (client) => {
  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${client.id}</td>
    <td>${client.surname}</td>
    <td>${client.firstname}</td>
    <td>${client.email || "—"}</td>
    <td>${client.birth_date || "—"}</td>
    <td><button class="btn" data-action="details" data-client-id="${client.id}">Подробнее</button></td>
    <td><button class="btn secondary" data-action="edit" data-client-id="${client.id}">Редактировать</button></td>
  `;

  row.querySelector('button[data-action="details"]').addEventListener("click", () => openDetails(client.id));
  row.querySelector('button[data-action="edit"]').addEventListener("click", () => openEdit(client.id));
  tableBody.appendChild(row);
};

const loadClients = async () => {
  hideMessage();
  tableBody.innerHTML = "";

  try {
    const response = await fetch("/api/clients");
    if (!response.ok) {
      throw new Error("Не удалось загрузить список клиентов");
    }

    const clients = await response.json();
    if (!clients.length) {
      showMessage("Клиенты не найдены");
      return;
    }

    clients.forEach(renderRow);
  } catch (error) {
    showMessage(error.message, true);
  }
};

document.addEventListener("DOMContentLoaded", loadClients);

const openCreateWindow = () => {
  window.open("new_client.html", "_blank", "width=600,height=700");
};

createBtn.addEventListener("click", openCreateWindow);

window.addEventListener("message", (event) => {
  if (event.data === "client-added" || event.data === "client-updated") {
    loadClients();
  }
});
