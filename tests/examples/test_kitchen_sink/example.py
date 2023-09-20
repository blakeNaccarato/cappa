#!/usr/bin/env python

from __future__ import annotations

import enum
import logging
import sqlite3
from dataclasses import dataclass, field
from typing import List, Literal, Union

from cappa import Arg, Dep, Subcommand, command, invoke, parse
from typing_extensions import Annotated

log = logging.getLogger(__name__)


class OtherOptions(enum.Enum):
    a = "a"
    b = "b"
    c = "c"


@dataclass
class Example:
    """Example program.

    Args:
       name: Required name argument
       flag: optional flag to enable
    """

    name: str
    value: Annotated[int, Arg(short="-V", long="--val", default=0)]

    options: Annotated[
        Union[Literal["one"], Literal["two"], Literal[3]], Arg(short=True)
    ]
    moptions: Annotated[OtherOptions, Arg(short=True)]

    subcommand: Annotated[Union[MeowCommand, BarkCommand], Subcommand]

    flags: Annotated[List[str], Arg(short=True, long=True)] = field(
        default_factory=list
    )
    flag: bool = False  # --flag


def db() -> sqlite3.Connection:
    return sqlite3.connect("sqlite:///")


def meow(
    command: Example,
    meow: MeowCommand,
    db: Annotated[sqlite3.Connection, Dep(db)],
):
    result = db.execute(f"select '{command.name}', {meow.times} + 1").fetchone()
    log.info(result)


@command(name="meow", invoke=meow)
@dataclass
class MeowCommand:
    times: int


def bark(bark: BarkCommand):
    log.info(bark)


@command(name="bark", invoke=bark)
@dataclass
class BarkCommand:
    ...


# invoke cli parsing
def main(argv=None):
    logging.basicConfig()

    args: Example = parse(Example, argv=argv, version="1.2.3")
    log.info(args)

    invoke(Example, argv=argv, version="1.2.3")


if __name__ == "__main__":
    main()
