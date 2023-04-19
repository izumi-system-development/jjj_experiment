from jjjexperiment.result import ResultSummary

def generate_test_validations(txt, result: ResultSummary, base_result: ResultSummary) -> None:
    """ テストコードのバリデーション値スニペットを生成
        テストコードを記述するのに使用しています
    """
    with open(txt + '.txt', 'w') as f:
        if result.q_rtd_H != base_result.q_rtd_H:
            f.write("q_rtd_H == " + str(result.q_rtd_H) + "\n")
        if result.q_rtd_C != base_result.q_rtd_C:
            f.write("q_rtd_C == " + str(result.q_rtd_C) + "\n")

        if result.q_max_H != base_result.q_max_H:
            f.write("q_max_H == " + str(result.q_max_H) + "\n")
        if result.q_max_C != base_result.q_max_C:
            f.write("q_max_C == " + str(result.q_max_C) + "\n")

        if result.e_rtd_H != base_result.e_rtd_H:
            f.write("e_rtd_H == " + str(result.e_rtd_H) + "\n")
        if result.e_rtd_C != base_result.e_rtd_C:
            f.write("e_rtd_C == " + str(result.e_rtd_C) + "\n")

        if result.E_H != base_result.E_H:
            f.write("E_H == " + str(result.E_H) + "\n")
        if result.E_C != base_result.E_C:
            f.write("E_C == " + str(result.E_C) + "\n")
