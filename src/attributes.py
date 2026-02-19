import pymupdf

def GET_ATTRIBUTES(pdf):
    WIDGETS = {
        'MU_1': 8,
        'KL_1': 8,
        'IN_1': 8,
        'CH_1': 8,
        'FF_1': 8,
        'GE_1': 8,
        'KO_1': 8,
        'KK_1': 8
    }
    
    with pymupdf.open(pdf) as doc:
        PAGE = doc[0]

        for widget in PAGE.widgets():
            if widget.field_name in WIDGETS.keys():
                WIDGETS[widget.field_name] = int(widget.field_value)
        return WIDGETS
