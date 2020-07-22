# -*- coding: utf-8 -*-

"""
flake8 plugin which verifies that all functions are called with arg=value (and not only with value).
"""

import ast
import re


FCFN001 = (
    "FCFN001: [{f_name}] function should be called with keywords arguments. {values}"
)


class FunctionCallForceNames(object):
    """
    flake8 plugin which verifies that all functions are called with arg=value (and not only with value).
    """

    name = "FunctionCallForceNames"
    version = "1.0.0"

    def __init__(self, tree, lines):
        self.tree = tree
        self.lines = lines

    @classmethod
    def add_options(cls, option_manager):
        option_manager.add_option(
            long_option_name="--fcfn_exclude_functions",
            default="",
            parse_from_config=True,
            comma_separated_list=True,
            help="Functions to exclude from checking.",
        )

    @classmethod
    def parse_options(cls, options):
        cls.exclude_functions = options.fcfn_exclude_functions

    def _get_values(self, args_):
        values = ""
        for arg in args_:
            if isinstance(arg, ast.JoinedStr):
                for val in arg.values:
                    if isinstance(val, ast.FormattedValue):
                        continue

                    values += f"value: {self._get_func_name(elm=val)} (line:{arg.lineno} column:{arg.col_offset})"

            if isinstance(arg, ast.Dict):
                values += (
                    f"value:  {ast.Dict} (line:{arg.lineno} column:{arg.col_offset})"
                )

            else:
                values += (
                    f"value: {self._get_func_name(elm=arg)} "
                    f"(line:{arg.lineno} column:{arg.col_offset})"
                )
        return values

    def _get_elm_func_id(self, elm, attr=False):
        if attr:
            elm_func_attr = getattr(elm, "attr", None)
            if elm_func_attr:
                yield elm_func_attr

        if isinstance(elm, ast.With):

            def _parse_name(lineno):
                name = re.findall(r"[a-z].*\(|[A-Z].*\(", lineno.strip())
                if not name:
                    _parse_name(lineno=self.lines[elm.lineno])
                return name

            name = _parse_name(lineno=self.lines[elm.lineno - 1])
            if name:
                yield name[0].strip("(").strip("with ")

            for elm_body in elm.body:
                if (
                    isinstance(elm_body, ast.Call)
                    or isinstance(elm_body, ast.Expr)
                    or isinstance(elm_body, ast.Assign)
                ):
                    yield from self._get_elm_func_id(elm=elm_body, attr=attr)

        elm_func_id = getattr(elm, "id", None)
        if elm_func_id:
            yield elm_func_id

        elm_func_s = getattr(elm, "s", None)
        if elm_func_s:
            yield elm_func_s

        elm_val_func = getattr(elm, "func", None)
        if elm_val_func:
            yield from self._get_elm_func_id(elm=elm_val_func, attr=attr)

        elm_val = getattr(elm, "value", None)
        if elm_val:
            yield from self._get_elm_func_id(elm=elm_val, attr=attr)

    def _get_func_name(self, elm, attr=True):
        for name in self._get_elm_func_id(elm=elm, attr=attr):
            if not name:
                for name in self._get_elm_func_id(elm=elm, attr=not attr):
                    if name:
                        return name

            return name

    def _skip_function_from_check(self, elm):
        name = self._get_func_name(elm=elm, attr=False)
        if name not in self.exclude_functions:
            if name and isinstance(name, str):
                for _name in name.split("."):
                    if _name in self.exclude_functions:
                        return True
            return self._get_func_name(elm=elm) in self.exclude_functions

        return name in self.exclude_functions

    @staticmethod
    def _get_args(elm):
        res = {}
        if getattr(elm, "value", None):
            _args = getattr(elm.value, "args", [])
            _args = [
                ar
                for ar in _args
                if not (isinstance(ar, ast.Starred) or isinstance(ar, ast.JoinedStr))
            ]
            if _args:
                res[elm] = _args

        if isinstance(elm, ast.With):
            for item in elm.items:
                if isinstance(item.context_expr, ast.Call):
                    _args = getattr(item.context_expr, "args", [])
                    _args = [
                        ar
                        for ar in _args
                        if not (
                            isinstance(ar, ast.Starred) or isinstance(ar, ast.JoinedStr)
                        )
                    ]
                    if _args:
                        res[item.context_expr] = _args

        return res

    def _missing_keywords(self, elm):
        if self._skip_function_from_check(elm=elm):
            return

        elm_and_args = self._get_args(elm=elm)
        if not elm_and_args:
            return

        name = self._get_func_name(elm=elm)
        for elm_key, args_key in elm_and_args.items():
            values = self._get_values(args_=args_key)
            if values:
                yield (
                    getattr(elm_key, "lineno", None) or elm.value.lineno,
                    getattr(elm_key, "col_offset", None) or elm.value.col_offset,
                    FCFN001.format(f_name=name, values=values),
                    self.name,
                )

    def _get_final_elm(self, elm):
        if getattr(elm, "body", None):
            for el in elm.body:
                if getattr(el, "body", None):
                    yield from self._get_final_elm(elm=el)

                yield el
        else:
            yield elm

    def _get_func_call(self):
        for elm in self._get_final_elm(elm=self.tree):
            if (
                isinstance(elm, ast.Expr)
                or isinstance(elm, ast.Call)
                or isinstance(elm, ast.Assign)
                or isinstance(elm, ast.With)
            ):
                yield elm

    def run(self):
        for elm in self._get_func_call():
            yield from self._missing_keywords(elm=elm)
