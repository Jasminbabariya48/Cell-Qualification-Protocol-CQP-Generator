def extract_tests_from_table(table):
    # Parse test parameter rows from ACL table
    tests = []
    for row_idx, row in enumerate(table.rows):
        cells = [cell.text.strip() for cell in row.cells]
        
        if len(cells) < 3:
            continue
            
        try:
            sr_no_str = cells[0].replace(".", "").strip()
            sr_no = int(sr_no_str)
            
            parameter = cells[1]
            acceptance_limit = cells[2]
            clause = cells[3] if len(cells) > 3 else ""
            
            tests.append({
                "sr_no": sr_no,
                "parameter": parameter,
                "acceptance_limit": acceptance_limit,
                "clause": clause
            })
        except ValueError:
            # Skip non-numeric header rows
            pass
            
    return tests
