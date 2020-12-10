import click
import sys
import colored
import logging


import coloredlogs


__SYNTHPY = r"""
Welcome to
                     _   _                 
     ___ _   _ _ __ | |_| |__  _ __  _   _ 
    / __| | | | '_ \| __| '_ \| '_ \| | | |
    \__ \ |_| | | | | |_| | | | |_) | |_| |
    |___/\__, |_| |_|\__|_| |_| .__/ \__, |
         |___/                |_|    |___/    version: {version}
"""


@click.command()
@click.option(
    "--host",
    type=str,
    help="the synthd host (default: localhost:8182)",
    default="localhost:8182",
)
@click.option(
    "--namespace", type=str, help="the default namespace to prefix all requests with"
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "WARNING", "ERROR"]),
    default="WARNING",
    help="the desired logging verbosity (default: WARNING)",
)
@click.option(
    "--ipython",
    is_flag=True,
    default=False,
    help="wether to use synthpy with IPython (requires IPython)",
)
@click.pass_context
def shell(ctx, host, namespace, log_level, ipython):
    import synthpy
    from synthpy import (
        Synth,
        Array,
        Field,
        OneOf,
        Object,
        Faker,
        DateTime,
        Categorical,
        Bool,
        Number,
        SameAs,
        String,
    )

    client_name = "synth"
    client_name_ = colored.stylize(client_name, colored.attr("bold"))
    header = f"{__SYNTHPY}\nGet started by accessing the client at the variable '{client_name_}'.\n\n".format(
        version=synthpy.__version__,
    )
    footer = ""

    logger = logging.getLogger("synthpy")
    coloredlogs.install(level=log_level)

    defaults = {}
    if namespace:
        defaults["namespace"] = namespace

    with Synth(host, defaults=defaults) as client:
        scope_vars = {
            client_name: client,
            "Array": Array,
            "Field": Field,
            "OneOf": OneOf,
            "Object": Object,
            "Faker": Faker,
            "DateTime": DateTime,
            "Categorical": Categorical,
            "Bool": Bool,
            "Number": Number,
            "SameAs": SameAs,
            "String": String,
        }

        if ipython:
            import IPython

            print(header)
            IPython.start_ipython(argv=[], user_ns=scope_vars)
            print(footer)

        else:
            from code import InteractiveConsole
            from colored import stylize_interactive, fg

            sys.ps1 = stylize_interactive("synthpy> ", fg("magenta"))
            InteractiveConsole(locals=scope_vars).interact(
                banner=header, exitmsg=footer
            )


if __name__ == "__main__":
    shell()
