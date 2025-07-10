const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");

const API_KEY = "AIzaSyAiKXdZLlKEckvn-pEx13_3Fm5bz__XD7U";
const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`;

const userData = {
  message: null,
};

// famoronana hafatra
const createMessageElement = (content, ...classes) => {
  const div = document.createElement("div");
  div.classList.add("message", ...classes);
  div.innerHTML = content;
  return div;
};

const generateBotResponse = async (incomingMessageDiv) => {
    const messageElement = incomingMessageDiv.querySelector(".message-text");
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [
        {
          parts: [
            {
              text: userData.message,
            }
          ]
        }
      ]
    })
  }

  try {
    const response = await fetch(API_URL, requestOptions);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error.message);

    const apiResponseText = data.candidates[0].content.parts[0].text.replace(/\*(.*?)\*\*/g, "$1").trim();
    incomingMessageDiv.innerText = apiResponseText;

  } catch (error) {
    console.log(error);
  } finally {
    incomingMessageDiv.classList.remove("thinking");
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
  }
}

// hafatra ny piditra...
const handleOutgoingMessage = (e) => {
  e.preventDefault();

  userData.message = messageInput.value.trim();
  messageInput.value = "";

  const messageContent = `<div class="message-text"></div>`;
  const outgoingMessageDiv = createMessageElement(
    messageContent,
    "user-message"
  );
  outgoingMessageDiv.querySelector(".message-text").textContent =
    userData.message;
  chatBody.appendChild(outgoingMessageDiv);
  chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

  setTimeout(() => {
    const messageContent = `<div class="message-text">
            <div class="thinking-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
          </div>`;
    const incomingMessageDiv = createMessageElement(
      messageContent,
      "bot-message",
      "thinking"
    );
    chatBody.appendChild(incomingMessageDiv);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
    generateBotResponse(incomingMessageDiv);
  }, 600);
};

messageInput.addEventListener("keydown", (e) => {
  const userMessage = e.target.value.trim();
  if (e.key == "Enter" && userMessage) {
    handleOutgoingMessage(e);
  }
});

sendMessageButton.addEventListener("click", (e) => handleOutgoingMessage(e));
