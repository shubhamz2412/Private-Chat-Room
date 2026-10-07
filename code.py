from nicegui import ui
from datetime import datetime

rooms = {
    "SHUBHAM": []
}


def get_room(room_name):
    room_name = room_name.strip().upper()

    if not room_name:
        room_name = "SHUBHAM"

    if room_name not in rooms:
        rooms[room_name] = []

    return room_name


@ui.page("/")
def chat_page():

    current_room = {"name": "SHUBHAM"}

    # ---------- FUNCTIONS ----------

    def render_messages():
        messages_box.clear()

        with messages_box:
            messages = rooms.get(current_room["name"], [])

            if not messages:
                ui.label("No messages yet").classes(
                    "text-gray-400 text-center w-full mt-10"
                )

            for msg in messages:

                is_me = msg["name"] == name_input.value.strip()

                with ui.row().classes(
                    "w-full justify-end" if is_me else "w-full justify-start"
                ):

                    with ui.column().classes(
                        "max-w-[75%] p-3 rounded-2xl "
                        + (
                            "bg-blue-500 text-white"
                            if is_me
                            else "bg-gray-100 text-gray-800"
                        )
                    ):

                        ui.label(msg["name"]).classes(
                            "text-xs font-bold opacity-70"
                        )

                        ui.label(msg["text"]).classes(
                            "text-base break-words"
                        )

                        ui.label(msg["time"]).classes(
                            "text-[10px] opacity-60 self-end"
                        )

    def join_room():

        room = get_room(room_input.value)

        current_room["name"] = room

        room_label.text = f"Room: {room}"

        render_messages()

        ui.notify(
            f"Joined room: {room}",
            type="positive"
        )

    def send_message():

        text = message_input.value.strip()

        name = name_input.value.strip()

        if not name:
            ui.notify("Enter your name", type="warning")
            return

        if not text:
            return

        room = current_room["name"]

        rooms[room].append({
            "name": name,
            "text": text,
            "time": datetime.now().strftime("%I:%M %p")
        })

        message_input.value = ""

        render_messages()

    # ---------- UI ----------

    ui.add_head_html("""
   <style>
    body {
        margin: 0;
        background-image: url("https://cdn.esahubble.org/archives/images/thumb300y/heic0411a.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
</style>
    """)

    with ui.column().classes(
        "w-full max-w-3xl mx-auto h-screen bg-white shadow-lg"
    ):

        # HEADER
        with ui.row().classes(
            "w-full items-center justify-between "
            "px-5 py-4 bg-blue-600 text-white"
        ):

            with ui.column().classes("gap-0"):

                ui.label("Made by Shubham").style(
                    "color: #0096FF; font-size: 18px; font-weight: 800;"
                )

                ui.label("Private Chat").classes(
                    "text-xl font-bold"
                )

                room_label = ui.label(
                    "Room: Kesa Lag Raha Hai"
                ).classes(
                    "text-xs opacity-80"
                )

            ui.label("● Online").classes(
                "text-sm"
            )

        # SETTINGS
        with ui.row().classes(
            "w-full px-4 pt-4 gap-2"
        ):

            name_input = ui.input(
                "Your Name"
            ).classes(
                "flex-1"
            )

            room_input = ui.input(
                "Room Name"
            ).classes(
                "flex-1"
            )

            ui.button(
                "Join",
                on_click=join_room
            ).classes(
                "bg-gold-600 text-white"
            )

        # MESSAGES
        messages_box = ui.column().classes(
            "flex-1 w-full overflow-auto px-4 py-4"
        )

        # MESSAGE INPUT
        with ui.row().classes(
            "w-full p-4 border-t gap-2"
        ):

            message_input = ui.input(
                "apki bari..."
            ).classes(
                "flex-1"
            )

            ui.button(
                "Send",
                on_click=send_message
            ).classes(
                "bg-blue-600 text-white"
            )

        # ENTER KEY
        message_input.on(
            "keydown.enter",
            send_message
        )

        # AUTO REFRESH
        ui.timer(
            0.5,
            render_messages
        )

        render_messages()


ui.run(
    host="0.0.0.0",
    port=8081,
    title="Private Chat",
    reload=False
)