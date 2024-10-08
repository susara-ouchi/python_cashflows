"""The main Space in the :mod:`~basiclife.BasicTerm_S` model.

:mod:`~basiclife.BasicTerm_S.Projection` is the only Space defined
in the :mod:`~basiclife.BasicTerm_S` model, and it contains
all the logic and data used in the model.

.. rubric:: Parameters and References

(In all the sample code below,
the global variable ``Projection`` refers to the
:mod:`~basiclife.BasicTerm_S.Projection` Space.)

Attributes:

    point_id: The ID of the selected model point.
        ``point_id`` is defined as a Reference, and its value
        is used for determining the selected model point.
        By default, ``1`` is assigned. To select another model point,
        assign its model point ID to it::

            >>> Projection.point_id = 2

        ``point_id`` is also defined as the parameter of the
        :mod:`~basiclife.BasicTerm_S.Projection` Space,
        which makes it possible to create dynamic child space
        for multiple model points::

            >>> Projection.parameters
            ('point_id',)

            >>> Projection[1]
            <ItemSpace BasicTerm_S.Projection[1]>

            >>> Projection[2]
            <ItemSpace BasicTerm_S.Projection[2]>

        .. seealso::

           * :attr:`model_point_table`
           * :func:`model_point`

    model_point_table: All model point data as a DataFrame.
        The sample model point data was generated by
        *generate_model_points.ipynb* included in the library.
        The DataFrame has an index named ``point_id``,
        and :func:`model_point` returns a record as a Series
        whose index value matches :attr:`point_id`.
        The DataFrame has columns labeled ``age_at_entry``,
        ``sex``, ``policy_term``, ``policy_count``
        and ``sum_assured``.
        Cells defined in :mod:`~basiclife.BasicTerm_S.Projection`
        with the same names as these columns return
        the corresponding column's values for the selected model point.
        (``policy_count`` is not used by default.)

        .. code-block::

            >>> Projection.model_poit_table
                       age_at_entry sex  policy_term  policy_count  sum_assured
            point_id
            1                    47   M           10             1       622000
            2                    29   M           20             1       752000
            3                    51   F           10             1       799000
            4                    32   F           20             1       422000
            5                    28   M           15             1       605000
                            ...  ..          ...           ...          ...
            9996                 47   M           20             1       827000
            9997                 30   M           15             1       826000
            9998                 45   F           20             1       783000
            9999                 39   M           20             1       302000
            10000                22   F           15             1       576000

            [10000 rows x 5 columns]

        The DataFrame is saved in the Excel file *model_point_table.xlsx*
        placed in the model folder.
        :attr:`model_point_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.model_point_table._mx_dataclient
            <PandasData path='model_point_table.xlsx' filetype='excel'>

        .. seealso::

           * :attr:`point_id`
           * :func:`model_point`
           * :func:`age_at_entry`
           * :func:`sex`
           * :func:`policy_term`
           * :func:`sum_assured`


    disc_rate_ann: Annual discount rates by duration as a pandas Series.

        .. code-block::

            >>> Projection.disc_rate_ann
            year
            0      0.00000
            1      0.00555
            2      0.00684
            3      0.00788
            4      0.00866

            146    0.03025
            147    0.03033
            148    0.03041
            149    0.03049
            150    0.03056
            Name: disc_rate_ann, Length: 151, dtype: float64

        The Series is saved in the Excel file *disc_rate_ann.xlsx*
        placed in the model folder.
        :attr:`disc_rate_ann` is created by
        Projection's `new_pandas`_ method,
        so that the Series is saved in the separate file.
        The Series has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.disc_rate_ann._mx_dataclient
            <PandasData path='disc_rate_ann.xlsx' filetype='excel'>

        .. seealso::

           * :func:`disc_rate_mth`
           * :func:`disc_factors`

    mort_table: Mortality table by age and duration as a DataFrame.
        See *basic_term_sample.xlsx* included in this library
        for how the sample mortality rates are created.

        .. code-block::

            >>> Projection.mort_table
                        0         1         2         3         4         5
            Age
            18   0.000231  0.000254  0.000280  0.000308  0.000338  0.000372
            19   0.000235  0.000259  0.000285  0.000313  0.000345  0.000379
            20   0.000240  0.000264  0.000290  0.000319  0.000351  0.000386
            21   0.000245  0.000269  0.000296  0.000326  0.000359  0.000394
            22   0.000250  0.000275  0.000303  0.000333  0.000367  0.000403
            ..        ...       ...       ...       ...       ...       ...
            116  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            117  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            118  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            119  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000
            120  1.000000  1.000000  1.000000  1.000000  1.000000  1.000000

            [103 rows x 6 columns]

        The DataFrame is saved in the Excel file *mort_table.xlsx*
        placed in the model folder.
        :attr:`mort_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.mort_table._mx_dataclient
            <PandasData path='mort_table.xlsx' filetype='excel'>

        .. seealso::

           * :func:`mort_rate`
           * :func:`mort_rate_mth`

    np: The `numpy`_ module.
    pd: The `pandas`_ module.

.. _numpy:
   https://numpy.org/

.. _pandas:
   https://pandas.pydata.org/

.. _new_pandas:
   https://docs.modelx.io/en/latest/reference/space/generated/modelx.core.space.UserSpace.new_pandas.html

"""

from modelx.serialize.jsonvalues import *

_formula = lambda : None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def COMM(t): 
    """Total commission"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (COMM_INIT(t) + COMM_REN(t))


def COMM_INIT(t): 
    """Initial commission"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (Input.DUR_M(t) == 1) * PREM_PAYBL_M(t) * Input.COMM_RATE(t)


def COMM_REN(t): 
    """Renewal commission"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (Input.DUR_M(t) > 1) * PREM_PAYBL_M(t) * Input.COMM_RATE(t)


def DTH_BEN(t):
    """Death claims"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return IND_ACTIVE_POL(t) * Input.SUM_ASSURED() * POLS_DTH(t)


def EXPS(t):
    """Total expenses accounting for acquisition,
        maintenance and claim expenses"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (EXPS_ACQ(t)
                + EXPS_MAINT(t)
                + EXPS_CLAIM_DTH(t)
                + EXPS_CLAIM_SURR(t)
                + EXPS_CLAIM_MAT(t))


def EXPS_ACQ(t):
    """Acquisition expense per policy"""

    if t != 1:
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        i        = Input.Exp_Acq_A["Fixed"]
        per_prem = Input.Exp_Acq_A["% of Premium"]
        per_sa   = Input.Exp_Acq_A["% of SA"]
        exp_acq = i + per_prem * Input.PREM_PP() + per_sa * Input.SUM_ASSURED()
        return exp_acq * (Input.DUR_M(t) == 1)


def EXPS_CLAIM_DTH(t):
    """Expenses incured at death"""
    flag = (Input.DUR_M(t) <= Input.POL_TERM_M() + 1)
    ## Inflation adjustment for EOM

    return flag * Input.Exp_Claim_A["Fixed"] * POLS_DTH(t) * Input.INFL_FAC(t+1, "Locked")


def EXPS_CLAIM_MAT(t):
    """Expenses incured at maturity"""
    flag = (Input.DUR_M(t) <= Input.POL_TERM_M() + 1)

    return flag * Input.Exp_Claim_A["Fixed"] * POLS_MAT(t) * Input.INFL_FAC(t, "Locked")


def EXPS_CLAIM_SURR(t):
    """Expenses incured at surrender"""
    flag = IND_ACTIVE_POL(t) * (SURR_BEN(t) > 0)
    ## Inflation adjustment for EOM

    return flag * Input.Exp_Claim_A["Fixed"] * POLS_LAPSE(t) * Input.INFL_FAC(t+1, "Locked")


def EXPS_MAINT(t):
    """Annual maintenance expense per policy"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        e           = Input.Exp_Maint_A["Fixed"]/12 * Input.INFL_FAC(t, "Locked")
        per_prem    = Input.Exp_Maint_A["% of Premium"]

        return IND_ACTIVE_POL(t) * (e + per_prem * Input.PREM_PP()/12) * POLS_IF(t) * (Input.DUR_M(t) != 1)


def GSV(t):
    """Guaranteed Surrender Value"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        n = Input.GSVFactors.index.max()
        y = Input.np.minimum(((Input.DUR_M(t))/12).apply(Input.math.ceil), n)
        GSVFac = ((Input.PREM_TERM_Y() == 6) * list(Input.GSVFactors["6-PPT"][y])
              + (Input.PREM_TERM_Y() == 12) * list(Input.GSVFactors["12-PPT"][y]))

    return y * GSVFac * Input.PREM_PP()


def INCM_BEN(t):
    """Expected income benefit:
        best estimate"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return INCM_VAL(t) * POLS_IF(t)


def INCM_VAL(t):
    """Income benefit amount"""

    if t <= 0:
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return Input.INCM_FAC(t) * Input.PREM_PP()/12 * IND_ACTIVE_POL(t)


def IND_ACTIVE_POL(t):
    """Indicator if the policy is active"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (Input.DUR_M(t) <= Input.POL_TERM_M())


def IND_ACTIVE_PREM(t):
    """Indicator if the premium term is active"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (Input.DUR_M(t) <= Input.PREM_TERM_M())


def INS_AFT_PROB(t):
    """Investment Component after probability"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return INS_BEF_PROB(t) * POLS_DTH(t)


def INS_BEF_PROB(t):
    """Insurance Expense"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return Input.np.maximum(0, (Input.SUM_ASSURED() + INCM_VAL(t)) * IND_ACTIVE_POL(t) - INV_BEF_PROB(t))


def INV_AFT_PROB(t):
    """Insurance expense after probability"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (DTH_BEN(t)
                + SURR_BEN(t)
                + INCM_BEN(t)
                + MAT_BEN(t)
                - INS_AFT_PROB(t))


def INV_BEF_PROB(t):
    """Investment Component"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        flag = (Input.DUR_M(t) == Input.POL_TERM_M() + 1)
        return (Input.np.maximum(SURR_VAL(t), Input.TERMINAL_BEN() * flag) + INCM_VAL(t))


def MAT_BEN(t):
    """Maturity benefit"""

    return Input.TERMINAL_BEN() * POLS_MAT(t)


def NET_CF(t):
    """Net cashflow"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (PREM_PAYBL_M(t)
            - DTH_BEN(t)
            - EXPS(t)
            - COMM(t)
            - SURR_BEN(t)
            - MAT_BEN(t)
            - INCM_BEN(t))


def POLS_DTH(t):
    """Number of death occurring at time t"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    elif t <= Input.VAL_M().max():
        ## simulating Actuals by increasing mortality
        return IND_ACTIVE_POL(t) * POLS_IF(t) * Input.MORT_RATE_MLY(t, "Locked") * 2
    else:
        return IND_ACTIVE_POL(t) * POLS_IF(t) * Input.MORT_RATE_MLY(t, "Previous")


def POLS_IF(t):
    """Number of policies in-force

    Currently the model is for new business so the
    initial value is read from :func:`pols_if_init`.
    Subsequent values are defined recursively."""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    elif t == 1:
        return Input.INIT_POLS_IF()
    else:
        flag = (Input.DUR_M(t) <= Input.POL_TERM_M() + 1)
        return flag * (POLS_IF(t-1) - POLS_DTH(t-1) - POLS_LAPSE(t-1) - POLS_MAT(t-1))


def POLS_LAPSE(t):
    """Number of lapse occurring at time t"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    elif t <= Input.VAL_M().max():
        ## simulating Actuals by increasing lapses
        return IND_ACTIVE_POL(t) * (POLS_IF(t) - POLS_DTH(t)) * Input.LAPSE_RATE_MLY(t) * 2
    else:
        return IND_ACTIVE_POL(t) * (POLS_IF(t) - POLS_DTH(t)) * Input.LAPSE_RATE_MLY(t)


def POLS_MAT(t):
    """Number of maturing policies

    The policy maturity occurs at ``t == 12 * policy_term()``,
    after death and lapse during the last period::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)

    otherwise ``0``."""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return (Input.DUR_M(t) == Input.POL_TERM_M() + 1) * (POLS_IF(t) - POLS_DTH(t) - POLS_LAPSE(t))


def PREM_PAYBL_M(t):
    """Monthly premium income

       Premium income during the period from ``t`` to ``t+1`` defined as::

       premium_pp(t)/premium frequency * pols_if(t)"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        return IND_ACTIVE_PREM(t) * Input.PREM_PP()/12 * POLS_IF(t)


def PV_DB(t):
    """Present value of death benefit
    for the calculation of surrender value"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        disc_fac = 1 + Input.DiscountRate["Locked"][Input.np.ceil(t/12)]
        mort1 = Input.MORT_RATE_MLY(t, "Locked")
        db = Input.SUM_ASSURED()/Input.PREM_PP()

        pv_db = db * mort1 / (disc_fac ** (1/24)) + PV_DB(t+12) * (1 - mort1)/disc_fac
        return IND_ACTIVE_POL(t) * pv_db


def PV_INCM_BEN(t):
    """Present Value of Income Benefit
    for the calculation of surrender value"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        disc_fac = 1 + Input.DiscountRate["Locked"][Input.np.ceil(t/12)]
        mort1 = Input.MORT_RATE_MLY(t, "Locked")


        pv_ib = Input.INCM_FAC(t)/(disc_fac ** (1/24)) + PV_INCM_BEN(t+12)/disc_fac
        return IND_ACTIVE_POL(t) * pv_ib * (1 - mort1)


def RA_MORT(t):
    """Risk adjustment: mortality"""

    if t <= 0 or t > Input.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Input.MP().index)
    else:
        y = Input.math.ceil(t/12)
        return DTH_BEN(t) * Input.RiskAdjustment["Mortality"][y]


def SSV(t):
    """Special surrender values"""

    y = (Input.DUR_M(t)/12).apply(Input.math.ceil)

    ratio = Input.np.minimum(1, y/Input.PREM_TERM_Y())
    return (PV_DB(t) + PV_INCM_BEN(t)) * ratio * Input.PREM_PP()


def SURR_BEN(t):
    """Surrender benefit"""

    return SURR_VAL(t) * POLS_LAPSE(t)


def SURR_VAL(t):
    """Surrender value
        defined as: Min(Max(SSV, GSV), 0.95 * SA)
        A factor is multiplied with SA to always have SURR_VAL < SA"""

    return Input.np.minimum(Input.np.maximum(SSV(t), GSV(t)), 0.95 * Input.SUM_ASSURED()) * (Input.DUR_M(t) > Input.SURR_TERM())


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("...", "Input"), "auto")