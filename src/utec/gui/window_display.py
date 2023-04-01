from apscheduler.schedulers.background import BaseScheduler
import pytermgui as ptg

from utec.gui.update_job import ScheduleUpdater
from utec.gui.progress_widget import ProgressWidget
from utec.gui.next_class_widget import NextClassWidget

import pytermgui as ptg


PALETTE_LIGHT = "#FCBA03"
PALETTE_MID = "#8C6701"
PALETTE_DARK = "#4D4940"
PALETTE_DARKER = "#242321"


def _create_aliases() -> None:
    ptg.tim.alias("app.text", "#cfc7b0")
    ptg.tim.alias("app.header", f"bold @{PALETTE_MID} #d9d2bd")
    ptg.tim.alias("app.header.fill", f"@{PALETTE_LIGHT}")
    ptg.tim.alias("app.title", f"bold {PALETTE_LIGHT}")
    ptg.tim.alias("app.button.label", f"bold @{PALETTE_DARK} app.text")
    ptg.tim.alias("app.button.highlight", "inverse app.button.label")
    ptg.tim.alias("app.footer", f"@{PALETTE_DARKER}")


def _configure_widgets() -> None:
    ptg.boxes.DOUBLE.set_chars_of(ptg.Window)
    ptg.boxes.ROUNDED.set_chars_of(ptg.Container)
    ptg.Button.styles.label = "app.button.label"
    ptg.Button.styles.highlight = "app.button.highlight"
    ptg.Slider.styles.filled__cursor = PALETTE_MID
    ptg.Slider.styles.filled_selected = PALETTE_LIGHT
    ptg.Label.styles.value = "app.text"
    ptg.Window.styles.border__corner = "#C2B280"
    ptg.Container.styles.border__corner = PALETTE_DARK
    ptg.Splitter.set_char("separator", "")  # type: ignore


def _define_layout() -> ptg.Layout:
    layout = ptg.Layout()
    layout.add_slot("Header", height=1)
    layout.add_break()
    layout.add_slot("Body")
    layout.add_break()
    # footer and two button spaces
    layout.add_slot("Footer Left", height=1, width=0.5)
    layout.add_slot("Footer Right", height=1, width=0.5)

    # layout.add_slot("Footer", height=1)

    return layout


def _confirm_quit(manager: ptg.WindowManager) -> None:
    modal = ptg.Window(
        "[app.title]Are you sure you want to quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(0)
    manager.add(modal)


def _confirm_reset(manager: ptg.WindowManager, updater: ScheduleUpdater):
    pbar = ProgressWidget()

    def reset_job_list_and_close() -> None:
        updater.refetch(pbar)
        modal.close()

    modal = ptg.Window(
        "[app.title]Are you sure you want to reset the job list?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: reset_job_list_and_close()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
            pbar
        ),
    ).center()

    modal.select(0)
    manager.add(modal)


def _daily_update(manager: ptg.WindowManager, updater: ScheduleUpdater) -> None:
    pbar = ProgressWidget()
    modal = ptg.Window(
            "[app.title]Updating job list...",
            "",
            ptg.Container(pbar)
        ).center()
    
    manager.add(modal)
    updater.refetch(pbar)
    modal.close()


def start_program(sched: BaseScheduler, updater: ScheduleUpdater) -> None:
    _create_aliases()
    _configure_widgets()
    sched.start()


    with ptg.WindowManager() as manager:
        def enable_daily_update() -> None:
            sched.add_job(_daily_update, 'cron', hour=6, minute=0, args=(manager, updater), id="daily_update")

        def disable_daily_update() -> None:
            sched.remove_job("daily_update")

        class_widget = NextClassWidget(sched=sched, every_seconds=1)

        manager.layout = _define_layout()
        header = ptg.Window(
            "[app.header] AutoClass ",
            box="EMPTY",
            is_persistant=True,
        )
        header.styles.fill = "app.header.fill"
        manager.add(header)

        footer_left = ptg.Window(
            ptg.Button("Quit", lambda *_: _confirm_quit(manager)),
            box="EMPTY",
        )
        footer_left.styles.fill = "app.footer"
        manager.add(footer_left, assign="footer_left")

        footer_right = ptg.Window(
            ptg.Button("Refresh", lambda *_: _confirm_reset(manager, updater)),
            box="EMPTY",
        )
        footer_left.styles.fill = "app.footer"
        manager.add(footer_right, assign="footer_right")

        manager.add(
            ptg.Window(
                "[app.title]Next class",
                "",
                class_widget,
                "",
                "",
                vertical_align=ptg.VerticalAlignment.TOP,
                overflow=ptg.Overflow.SCROLL,
            ),
            assign="body",
        )
