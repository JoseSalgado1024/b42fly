def kwargs_match(default, amend):
    return \
        {
            k: amend[k] if k in amend else v for k, v in default.items()
        }
