"""Details of the structure of txt files, extract data into objects with properties"""

def extractData(path, split_string):
    with path.open('r', encoding='utf8') as f:
        data = f.read()
        chunks = data.split(split_string)
        chunks = [ch.splitlines() for ch in chunks]
        # chunks = [[line.strip() for line in ch if line.strip()] for ch in chunks]
        chunks[0] = ['deleteme', '', *chunks[0]]
        chunks = [ch[1:] for ch in chunks][:-1]
        for chunk in chunks:
            yield chunk


def file_factory(path):
    with path.open('r', encoding='utf8') as f:
        header = f.readlines()[2].strip()
    assert header in ["Module Specification", "Programme Specification"]
    if header == "Module Specification":
        return ModuleFile(path)
    else:
        return ProgrammeFile(path)



def aggregate_until(data, end_item):
    result = []
    while True:
        if data[0].startswith(end_item):
            break
        row = data.pop(0).strip()
        if not row:
            continue
        result.append(row)
    return result


class Programme:
    def __init__(self, data):
        assert data[3] == "Programme Specification"
        assert data[9] == "Programme Full Title: "
        assert data[15] == "Programme Short Title: "
        self.full_title = data[11]
        self.short_title = data[13]
        assert data[17] == "Programme Code: "
        assert data[19] == "Programme Type: "
        self.type = data[21]
        self.code = data[23]

        data = data[24:]
        self.something = "\n".join(aggregate_until(data, "Faculty: "))
        assert data[0] == "Faculty: "
        self.faculty = data[2]
        assert data[4] == "School: "
        self.faculty = data[6]
        assert data[8] == "Department: "
        self.department = data[10]
        assert data[12] == "Programme Leader: "
        self.programme_leader = data[14]
        assert data[16] == "Mode of Delivery: "
        assert data[18] == "Normal Duration: "
        self.mode = data[22]
        self.duration = data[20]
        assert data[24] == "Offered at the following sites:"

        data = data[25:]
        self.sites = aggregate_until(data, "Distance Learning availability:")
        assert data[0] == "Distance Learning availability: "
        _ = aggregate_until(data, 'Awards Available:')

        assert data[0] == "Awards Available:\t"
        award_keys = data[1].split('\t')
        data = data[2:]
        awards = aggregate_until(data, 'Relevant QAA subject benchmarking statement(s):')
        self.awards = [{k: v for k, v in zip(award_keys, a.split('\t'))} for a in awards]

        assert data[0] == "Relevant QAA subject benchmarking statement(s):"
        data = data[1:]
        self.qaa_benchmarking_statements = aggregate_until(data, 'Accreditation Details:')
        data = data[1:]
        self.accreditation_details = aggregate_until(data, "Entry Requirements")
        self.entry_requirements = aggregate_until(data, 'Programme Description')

        assert data[0] == "Programme Description: Characteristics and Aims"
        self.description = data[1].strip()
        assert data[3] == "Learning, Teaching and Assessment Strategies:"
        self.learning_teaching_and_assessment_strategies = data[4].strip()
        assert data[6] == "Structure and Regulations:"
        self.structure_and_regulations = data[7].strip()
        assert data[9] == "Learning Outcomes:"
        self.learning_outcomes = data[10].strip()
        data = data[12:]
        assert data[0].strip() == 'Module Details (across all module groups):'

        keys = data[1].split('\t')
        data = data[2:]
        values = aggregate_until(data, 'Any programme-specific differences or regulations:')
        self.modules = [{k: v for k, v in zip(keys, v.split('\t'))} for v in values]
        assert data == ['Any programme-specific differences or regulations:', '', '']

    def __str__(self):
        return f"Programme({self.code})"

    def corpora(self):
        return {
            "description": self.description,
            "learning_teaching_and_assessment_strategies": self.learning_teaching_and_assessment_strategies,
            "learning outcomes": self.learning_outcomes
        }


class Module:
    def __init__(self, data):
        assert data[3] == "Module Specification"
        assert data[9] == "Module Full Title: "
        assert data[15] == "Module Short Title: "
        assert data[17] == "Module Code: "
        assert data[19] == "Credit Value: "
        assert data[23] == "Credit Level: "
        assert data[29] == "Faculty: "
        assert data[33] == "School: "
        assert data[37] == "Department: "
        assert data[41] == "Module Leader: "
        assert data[45] == "Module Appraiser(s) / Marker(s): "

        self.full_title = data[11]
        self.short_name = data[13]
        self.credit_value = data[21]
        self.credit_level = data[25]
        self.code = data[27]
        self.faculty = data[31]
        self.school = data[35]
        self.department = data[39]
        self.module_leader = data[43]
        data = data[46:]

        self.module_appraisers = aggregate_until(data, "Offered at the following sites:")
        assert data[0] == "Offered at the following sites:"
        data = data[1:]

        self.sites = aggregate_until(data, "Semester / Year-long:")
        assert data[0] == "Semester / Year-long: "
        data = data[1:]

        self.intakes = aggregate_until(data, "DMUGlobal Content indicator:")

        assert data[0] == "DMUGlobal Content indicator: "
        assert data[2] in ["Y", "N"]
        self.DMUGlobal = data[2] == "Y"

        assert data[4] == "Ethical approval required: "
        assert data[6] in ["Y", "N"]
        self.ethical_approval = data[6] == "Y"

        assert data[8] == "Details of Accreditation by Professional, Statutory or Regulatory Body:"
        data = data[9:]
        self.accreditation = aggregate_until(data, "Module Pre-requisites:")
        assert data[0] == "Module Pre-requisites:"
        data = data[1:]

        self.prerequisites = aggregate_until(data, "Module Description:")
        assert data[0] == "Module Description:"
        assert data[3] == "Learning Outcomes:"

        self.description = data[1]
        self.learning_outcomes = data[4]

        assert data[6].strip() == "Evaluation:"

        assessment_keys = data[7].split('\t')
        data = data[8:]
        assert len(assessment_keys) == 8
        assessments = aggregate_until(data, "Anonymous marking exemption codes:")
        self.assessments = [{k: v for k, v in zip(assessment_keys, a.split('\t'))} for a in assessments]
        assert data[
                   0] == "Anonymous marking exemption codes: OPTO1: Individually distinct work; OPTO2: Reflection on development of own work; OPTO3:"

        assert data[3] == "Assessment Notes:"
        self.assessment_notes = data[4]

        assert data[6] == "Reassessment:"
        self.reassessment = data[7]

        assert data[9] == "Expected Methods of Delivery:"
        self.method_of_delivery = data[10]

        assert data[12].strip() == "Programmes using this module:"
        programme_keys = data[15].split('\t')
        data = data[16:]
        programmes = aggregate_until(data, "Remarks:")
        self.programmes = [{k: v for k, v in zip(programme_keys, p.split('\t'))} for p in programmes]
        # assert data == ["Remarks:", "", ""]
        assert data[0].strip() == "Remarks:"
        self.remarks = [remark for remark in data[1:] if remark]

    def corpora(self):
        """
        This method should return the main corpus for this module.
        Make adjustments here to control what we actually analyse.
        """
        return {
            "description": self.description
        }

    def __str__(self):
        return f"Module({self.code})"


class DataFile:
    stop = None    

    def __init__(self, path):
        self.path = path

    def __iter__(self):
        for d in extractData(self.path, self.stop):
            yield self.item_class(d)


class ProgrammeFile(DataFile):
    stop = 'End of Programme Specification for'
    type = 'programme'
    item_class = Programme


class ModuleFile(DataFile):
    stop = 'End of Module Specification for'
    type = 'module'
    item_class = Module
