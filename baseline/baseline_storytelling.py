def baseline_storytelling(tables, intention):
    reflection = reflection(tables)
    outline = outline(intention, reflection, tables)
    narrative = narrative(intention, tables, outline)
    return narrative