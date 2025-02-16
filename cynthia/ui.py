import gradio as gr

force_dark_mode = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""


def launch_chat_interface(chat_function):

    ui = gr.ChatInterface(
        fn=chat_function,
        type="messages",
        js=force_dark_mode,
    )

    ui.launch()
