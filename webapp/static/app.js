const messageBox = document.getElementById("message");
const tableBody = document.querySelector("#clients-table tbody");
const createBtn = document.getElementById("create-btn");
const filterForm = document.getElementById("filter-form");
const resetFiltersBtn = document.getElementById("reset-filters");

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

const openForm = (mode, id) => {
  const params = new URLSearchParams();
  params.set("mode", mode);
  if (id) params.set("id", id);
  window.open(`client_form.html?${params.toString()}`, "_blank", "width=600,height=700");
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
    <td><button class="btn danger" data-action="delete" data-client-id="${client.id}">Удалить</button></td>
  `;

  row.querySelector('button[data-action="details"]').addEventListener("click", () => openDetails(client.id));
  row.querySelector('button[data-action="edit"]').addEventListener("click", () => openForm("edit", client.id));
  row.querySelector('button[data-action="delete"]').addEventListener("click", () => deleteClient(client.id));
  tableBody.appendChild(row);
};

const getFilters = () => {
  const data = new FormData(filterForm);
  const params = new URLSearchParams();
  const minBalance = data.get("min_balance");
  const maxBalance = data.get("max_balance");
  const hasEmail = data.get("has_email");
  const surnamePrefix = data.get("surname_prefix");

  if (minBalance) params.set("min_balance", minBalance);
  if (maxBalance) params.set("max_balance", maxBalance);
  if (hasEmail) params.set("has_email", hasEmail);
  if (surnamePrefix) params.set("surname_prefix", surnamePrefix.trim());

  return params.toString();
};

const loadClients = async () => {
  hideMessage();
  tableBody.innerHTML = "";

  try {
    const query = getFilters();
    const url = query ? `/api/clients?${query}` : "/api/clients";
    const response = await fetch(url);
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

createBtn.addEventListener("click", () => openForm("create"));

window.addEventListener("message", (event) => {
  if (event.data === "client-added" || event.data === "client-updated") {
    loadClients();
  }
});

filterForm.addEventListener("submit", (event) => {
  event.preventDefault();
  loadClients();
});

resetFiltersBtn.addEventListener("click", () => {
  filterForm.reset();
  loadClients();
});

const deleteClient = async (id) => {
  const confirmed = confirm("Удалить клиента?");
  if (!confirmed) return;

  try {
    const response = await fetch(`/api/clients/${id}`, { method: "DELETE" });
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || "Не удалось удалить клиента");
    }
    showMessage("Клиент удален");
    loadClients();
  } catch (error) {
    showMessage(error.message, true);
  }
};
