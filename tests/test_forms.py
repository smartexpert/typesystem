import jinja2
import markupsafe

import typesystem

contact = typesystem.Schema(
    fields={
        "a": typesystem.Boolean(),
        "b": typesystem.String(max_length=10),
        "c": typesystem.Text(),
        "d": typesystem.Choice(
            choices=[("abc", "Abc"), ("def", "Def"), ("ghi", "Ghi")]
        ),
    }
)


forms = typesystem.Jinja2Forms(package="typesystem")


def test_form_rendering():
    form = forms.create_form(contact)

    html = str(form)

    assert html.count('<input type="checkbox" ') == 1
    assert html.count('<input type="text" ') == 1
    assert html.count("<textarea ") == 1
    assert html.count("<select ") == 1


def test_password_rendering():
    password_schema = typesystem.Schema(
        {"password": typesystem.String(format="password")}
    )

    form = forms.create_form(password_schema)
    form.validate(data={"password": "secret"})
    html = str(form)
    assert "secret" not in html


def test_form_html():
    form = forms.create_form(contact)

    markup = form.__html__()

    assert isinstance(markup, markupsafe.Markup)
    assert str(markup) == str(form)


def test_forms_from_directory(tmpdir):
    forms = typesystem.Jinja2Forms(directory=str(tmpdir))
    assert isinstance(forms.env.loader, jinja2.FileSystemLoader)


def test_forms_with_directory_override(tmpdir):
    forms = typesystem.Jinja2Forms(directory=str(tmpdir), package="typesystem")
    assert isinstance(forms.env.loader, jinja2.ChoiceLoader)
