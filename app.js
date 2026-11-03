const tg = window.Telegram?.WebApp;

tg?.ready();
tg?.expand();

const userId = tg?.initDataUnsafe?.user?.id || 10001;
const API = "";

async function refresh() {
  try {
    const response = await fetch(
      `${API}/api/state?user_id=${userId}`
    );
    const data = await response.json();

    document.querySelector("#balance").textContent =
      Number(data.balance).toFixed(4);

    document.querySelector("#rate").textContent =
      Number(data.rate).toFixed(2);
  } catch (error) {
    console.log("Сервер пока не подключён");
  }
}

document.querySelector("#mine").onclick = () => {
  alert("Майнинг работает автоматически!");
};

document.querySelector("#daily").onclick = async () => {
  const response = await fetch(`${API}/api/daily`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({user_id: userId})
  });

  const data = await response.json();
  alert(data.message);
  refresh();
};

document.querySelector("#upgrade").onclick = async () => {
  const response = await fetch(`${API}/api/upgrade`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({user_id: userId})
  });

  const data = await response.json();
  alert(data.message);
  refresh();
};

refresh();
setInterval(refresh, 5000);
