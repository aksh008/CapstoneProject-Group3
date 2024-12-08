import chainlit as cl
@cl.on_chat_start
async def start_chat():
    await cl.Message(content="Welcome! Please Type 'Ready' to start disease identification.").send()

@cl.on_message
async def on_message(msg: cl.Message):
    # Check if a file is attached
    images = await cl.AskFileMessage(
            content="Please upload a Image to begin!", accept=["image/*"]
        ).send()
    # if not msg.elements:
    #     await cl.Message(content="No file attached. Please upload a plant image.").send()
    #     return


    # Processing images exclusively
    # images = [file for file in msg.images if "image" in file.mime]

    # Read the first image
    with open(images[0].path, "r") as f:
        pass # image procesign logic here MobileVnet and LLM will generate output here will pass to last line 

    await cl.Message(content=f"Received {len(images)} image we will do Plant Disease identificaation here ").send()

