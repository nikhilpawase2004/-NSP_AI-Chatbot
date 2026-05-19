let voiceMode = false;


/* SEND MESSAGE */
async function sendMessage(){

    const input = document.getElementById("user-input");

    const fileInput = document.getElementById("file-input");

    const message = input.value.trim();

    if(message === "" && fileInput.files.length === 0){
        return;
    }

    const chatBox = document.getElementById("chat-box");


    /* USER MESSAGE */
    chatBox.innerHTML += `

        <div class="user-message">
            ${message}
        </div>

    `;


    /* FILE MESSAGE */
    if(fileInput.files.length > 0){

        chatBox.innerHTML += `

            <div class="user-message">
                📎 ${fileInput.files[0].name}
            </div>

        `;
    }


    const formData = new FormData();

    formData.append("message", message);

    if(fileInput.files.length > 0){

        formData.append("file", fileInput.files[0]);
    }


    input.value = "";


    /* TYPING EFFECT */
    const typingId = "typing-" + Date.now();

    chatBox.innerHTML += `

        <div class="bot-message" id="${typingId}">
            NSP Bot is typing...
        </div>

    `;

    chatBox.scrollTop = chatBox.scrollHeight;


    try{

        const response = await fetch("/chat", {

            method:"POST",

            body:formData
        });

        const data = await response.json();

        let botReply = data.response;


        /* CODE FORMAT */
        botReply = botReply.replace(
            /```([\s\S]*?)```/g,
            '<pre><code>$1</code></pre>'
        );

        botReply = botReply.replace(/\n/g, "<br>");


        document.getElementById(typingId).remove();


        /* BOT MESSAGE */
        chatBox.innerHTML += `

            <div class="bot-message">
                ${botReply}
            </div>

        `;


        /* VOICE REPLY */
        if(voiceMode){

            speak(data.response);

            voiceMode = false;
        }

    }

    catch(error){

        document.getElementById(typingId).remove();

        chatBox.innerHTML += `

            <div class="bot-message">
                Server Error
            </div>

        `;
    }


    fileInput.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;
}



/* ENTER BUTTON */
document.getElementById("user-input")
.addEventListener("keypress", function(event){

    if(event.key === "Enter"){

        sendMessage();
    }
});



/* VOICE INPUT */
function startVoice(){

    voiceMode = true;

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = function(event){

        document.getElementById("user-input").value =
        event.results[0][0].transcript;

        sendMessage();
    };

    recognition.start();
}



/* SPEAK BOT RESPONSE */
function speak(text){

    const speech = new SpeechSynthesisUtterance();

    speech.text = text;

    speech.volume = 1;

    speech.rate = 1;

    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}



/* TOGGLE HISTORY */
function toggleHistory(){

    const panel = document.getElementById("history-panel");

    panel.classList.toggle("active");

    if(panel.classList.contains("active")){

        loadHistory();
    }
}



/* LOAD HISTORY */
async function loadHistory(){

    const response = await fetch("/history");

    const data = await response.json();

    const historyList = document.getElementById("history-list");

    historyList.innerHTML = "";


    data.forEach(chat => {

        historyList.innerHTML += `

        <div class="history-item">

            <p>
                <strong>You:</strong><br>
                ${chat.message}
            </p>

            <p>
                <strong>Bot:</strong><br>
                ${chat.response}
            </p>

            <button
            class="delete-btn"
            onclick="deleteHistory(${chat.id})">
                Delete
            </button>

        </div>

        `;
    });
}



/* DELETE SINGLE HISTORY */
async function deleteHistory(id){

    await fetch(`/delete/${id}`, {

        method:"DELETE"
    });

    loadHistory();
}



/* DELETE ALL HISTORY */
async function deleteAllHistory(){

    await fetch("/delete_all", {

        method:"DELETE"
    });

    loadHistory();
}