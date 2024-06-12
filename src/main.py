"""Entry point."""
import sys  # pylint: disable=wrong-import-position
import asyncio

print("Starting...")

async def main():
    if sys.platform not in ["linux", "win32"]:
        print(f"The '{sys.platform}' is not supported.")
        sys.exit(1)
    if sys.version_info < (3, 11) or sys.version_info > (3, 12):
        print(f"This applicaiton requires Python 3.11+. Found: {sys.version}.")
        sys.exit(1)

    if len(sys.argv) > 1:
        if any(arg in sys.argv for arg in ["--text", "-t"]):
            from utils.terminal import terminal

            print("Add a text input:")
            text: str = terminal.read_text()
            print()
            print("Result:")
            print(text)
            sys.exit()

        if any(arg in sys.argv for arg in ["--list", "-l"]):
            from utils.terminal import terminal

            keys = terminal.Key.list()
            keys.sort(key=lambda x: x[1])
            for key in keys:
                print(f"{key[1]}: {key[0]}")
            sys.exit()

        if any(arg in sys.argv for arg in ["--key_press", "-k"]):
            from utils.terminal import terminal

            print("Press a key to display its code and name (press 'q' to finish):")
            key = terminal.read_key()
            while key != "q":
                print(f"{terminal.Key.code_of(key)}")
                key = terminal.read_key()
            sys.exit()

        if any(arg in sys.argv for arg in ["--sandbox", "-s"]):
            from time import sleep
            from utils.terminal import terminal

            def delay_2() -> str:
                sleep(2)
                return "Returned"

            # def delay_10() -> str:
            #     sleep(10)
            #     return "Returned"

            try:
                print("Testing the wait_for function:")
                await terminal.wait_for(delay_2, text="This should finish in 2 second...", timeout=4.0)
                print("Finished.")
                # await terminal.wait_for(delay_10, "This should timeout in 3 seconds...", timeout=4.0)
                # print("Timeout Gracefully.")
                # await terminal.wait_for(delay_10, "This should timeout in 3 seconds...", timeout=4.0, raise_error=True)
                # print("Shoild not be here.")
            except TimeoutError:
                print("Timeout Error!.")
            sys.exit()

        if any(arg in sys.argv for arg in ["--graph", "-g"]):
            import os
            import workflow

            print("Generating graph...")
            temp = workflow.build()
            absolute_path = os.path.abspath("../docs/graph.png")
            temp.get_graph().draw_mermaid_png(output_file_path=absolute_path)
            print(f"Graph generated at '{absolute_path}'.")
            sys.exit()

    if __name__ == "__main__":
        import workflow
        from utils.general import is_verbose # pylint: disable=import-error

        wkf = workflow.build(is_verbose)
        wkf.validate()
        wkf.invoke({}, debug=is_verbose)


asyncio.run(main())