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

_formula = lambda point_id: None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AGE(t):

    """The attained age at time t."""

    if t < 0:
        raise ValueError("t cannot be less than 0")
    elif t == 0:
        return AGE_AT_ENTRY()
    else:        
        n = Input.mort_table.index.max()
        return Input.np.minimum(AGE_AT_ENTRY() + DUR_Y(t), n)


def AGE_AT_ENTRY():

    """The age at entry of the selected model point"""

    return MP()["age_at_entry"]


def COB_PH(t):

    """Cost of Bonus to Policyholders"""

    if t < 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return ((DUR_M(t) < POL_TERM_M()) * ((cob.DECLRD_REV_BONUS(t+1) - cob.DECLRD_REV_BONUS(t)) * cob.COB_FAC_PP(t) * POLS_IF(t))
                + AS.TERMINAL_BON_DTH(t) * POLS_DTH(t)
                + AS.TERMINAL_BON_MAT(t) * POLS_MAT(t-1))


def COMM(t):

    """Commissions
        Best Estimate basis"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        n = Input.comm_rates.index.max()
        dur_m = list(Input.np.minimum(Input.np.ceil(DUR_M(t)/12), n))
        comm_rates = Input.comm_rates["Projection"][dur_m]

        return IND_ACTIVE(t) * PREM_PAYBL_M(t) * list(comm_rates)


def DISC_RATE_M(t):

    """Monthly discount rate:
        Best Estimate basis"""

    return (1 + Input.yield_curve["Discount Rates"][Input.math.ceil((t+1)/12)])**(1/12) - 1


def DTH_BEN(t):

    """Death claims
        Best Estimate basis

    After probability, including the Terminal bonus and declared bonus"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (Input.np.maximum(Input.np.maximum(SUM_ASSURED(), 10 * PREM_PP()), DUR_M(t) * 1.05 * (PREM_PP() / 12))
                + cob.DECLRD_REV_BONUS(t) 
                + AS.TERMINAL_BON_DTH(t)) * POLS_DTH(t)


def DUR_M(t):

    """Duration in force in months"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0:
        return MP()['dur_elapsed']
    else:
        return DUR_M(t-1) + 1


def DUR_Y(t):

    """Duration in force in years"""

    return DUR_M(t)//12


def ESTATE_ROLLUP(t):

    """Roll up of Estate"""

    if t <= 0 or t > PROJ_LEN().max():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (DUR_M(t) <= POL_TERM_M() + 1) * (ESTATE_ROLLUP(t-1) + PROFIT_AFT_TAX_AND_SH_TRNS(t) + INT_ESTATE(t))


def EXPS(t):

    """Total expenses accounting for acquisition,
        maintenance and claim expenses"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        acq   = EXPS_ACQ(t)
        maint = EXPS_MAINT(t) 
        claim = EXPS_CLAIM(t) 
        return IND_ACTIVE(t) * (acq + maint + claim)


def EXPS_ACQ(t):

    """Acquisition expense per policy"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        i        = Input.exp_acq["Fixed"]
        per_prem = Input.exp_acq["% of Premium"]
        per_sa   = Input.exp_acq["% of SA"]

        exp_acq = i + per_prem * PREM_PP() + per_sa * SUM_ASSURED()
        return exp_acq * (DUR_M(t-1) == 0)


def EXPS_CLAIM(t):

    """Expenses incured at death/surrender/maturity"""

    return IND_ACTIVE(t) * Input.exp_claim["Claims"] * INFL_FAC(t) * (POLS_DTH(t) + POLS_LAPSE(t) * (SURR_BEN(t) > 0))


def EXPS_MAINT(t):

    """Expenses maintenance
        Best Estimate basis"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        e           = Input.exp_maint["Fixed"]/12 * INFL_FAC(t)
        per_prem    = Input.exp_maint["% of Premium"]
        per_res     = 1 - (1 - Input.exp_maint["% of Reserve"]) ** (1/12)
        flag        = (DUR_M(t-1) > 0) * IND_ACTIVE(t)

        return flag * (e
                       + per_prem * PREM_PP()/12
                       + per_res * RESERVE_PP(t-1)) * POLS_IF(t-1)


def GSV(t):

    """Guaranteed Surrender Value"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        flag = (DUR_M(t) > Input.surr_start_term["Surrender Start"])
        return flag * (Input.ACB_FAC(t) * cob.DECLRD_REV_BONUS(t) + (DUR_M(t)/12) * Input.GSV_FAC(t) * PREM_PP())


def INCR_RESERVE(t):

    """Increase in reserves

    Increase in reserves at ``t`` is defined as:
        reserve_if(t) - reserve_if(t-1)
    """

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return RESERVE_IF(t) - RESERVE_IF(t-1)


def INCR_SOLVM(t):

    """Increase in solvency margin

    Increase in solvency margin at 't' is defined as:

        solvm_if(t) - solvm_if(t-1)"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (DUR_M(t) <= POL_TERM_M() + 1) * (SOLV_MARG_SH_FUNDED(t) - SOLV_MARG_SH_FUNDED(t-1))


def IND_ACTIVE(t):
    """Indicator if the policy is active

    defined as a series of boolean Duration(t) <= Policy_Term_M"""

    return (DUR_M(t) <= POL_TERM_M())


def INFL_FAC(t):

    """The inflation factor at time t"""

    if t < 0:
        raise ValueError("t cannot be less than zero.")
    elif t <= 1:
        return 1
    else:
        return (1 + INFL_RATE()) ** ((t-1)/12)


def INFL_RATE():

    """Inflation rate"""

    return Input.infl_rate["Inflation"]


def INIT_POLS_IF(): 

    """Initial Number of Policies In-force

    Number of in-force policies at time 0 referenced from :func:`pols_if`.
    Defaults to 1."""

    return Input.pd.Series(1, index = MP().index)


def INT_ESTATE(t):

    """Roll up of Estate"""

    if t <= 0 or t > PROJ_LEN().max():
        return Input.pd.Series(0, index = MP().index)
    else:
        i = (1 + Input.yield_curve["Interest Rates"][Input.math.ceil(t/12)] * (1 - Input.Tax_Rates["Policyholder"]) - Input.inv_exp_pc["Investment Expenses %"]) ** (1/12) - 1
        return (DUR_M(t) <= POL_TERM_M() + 1) * ESTATE_ROLLUP(t-1) * i


def INT_NET_CF(t):

    """Interest earned on net cashflows"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        y = Input.math.ceil(t/12)
        i = (1 + Input.yield_curve["Interest Rates"][y]) ** (1/12) - 1

        return (PREM_PAYBL_M(t)
                - EXPS_ACQ(t)
                - EXPS_MAINT(t)
                - COMM(t)) * i * IND_ACTIVE(t)


def INT_RESERVES(t):

    """Interest earned on reserves"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        i = (1 + Input.yield_curve["Interest Rates"][Input.math.ceil(t/12)]) ** (1/12) - 1

        return IND_ACTIVE(t) * RESERVE_IF(t-1) * i


def INT_SOLVM(t):

    """Interest earned on solvency margin

    Interest earned at ``t`` is defined as:
        solvm_if(t-1) * disc_rate_mth"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        i = (1 + Input.yield_curve["Interest Rates"][Input.math.ceil(t/12)]) ** (1/12) - 1

        return (DUR_M(t) <= POL_TERM_M() + 1) * SOLV_MARG_SH_FUNDED(t-1) * i


def INV_EXP_SOLVM(t):

    """Investment expense on solvency margin"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        y = Input.math.ceil(t/12)        
        fac = (1 + Input.yield_curve["Interest Rates"][y] - Input.inv_exp_pc["Investment Expenses %"]) ** (1/12) - 1
        return (DUR_M(t) <= POL_TERM_M() + 1) * (INT_SOLVM(t) - SOLV_MARG_SH_FUNDED(t-1) * fac)


def LAPSE_RATE(t):

    """Lapse rate
        Best Estimate"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        n = Input.lapse_table.index.max()
        dur_m = list(Input.np.minimum((DUR_M(t)/12).apply(Input.math.ceil), n))
        lapse_rates = Input.lapse_table["Projection"][dur_m]

        return Input.pd.Series(list(lapse_rates), index = MP().index)


def LAPSE_RATE_MLY(t):

    """Monthly Lapse rate to be applied at time t"""

    return 1 - (1 - LAPSE_RATE(t)) ** (1/12)


def MAT_BEN(t):

    """Maturity benefit"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0,index = MP().index)
    else:
        return (DUR_M(t) == POL_TERM_M() + 1) * (SUM_ASSURED() + cob.DECLRD_REV_BONUS(t-1)+ AS.TERMINAL_BON_MAT(t)) * POLS_MAT(t-1)


MAX_PROJ_LEN = lambda: PROJ_LEN().max()

def MORT_RATE_ANN(t):

    """Mortality rate to be applied at time t"""

    fac = Input.mort_scale["Rate"]
    return fac * Input.BASE_MORT_RATE(t)


def MORT_RATE_MLY(t):

    """Monthly mortality rate to be applied at time t"""

    return 1 - (1 - MORT_RATE_ANN(t)) ** (1/12)


def MP():

    """The selected model point as a Series"""

    if type(Input.point_id) == int:
        if Input.point_id == 0:
            return Input.model_point_table
        else:
            return Input.model_point_table.loc[[Input.point_id]]
    elif type(Input.point_id) == list:
        return Input.model_point_table.loc[Input.point_id]
    else:
        print(f"Incompatible data type for Input.point_id: {type(Input.point_id)}")
        raise ValueError


def NET_CF(t):

    """Net cashflow"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (PREM_PAYBL_M(t)
                + INT_NET_CF(t)
                - DTH_BEN(t)
                - EXPS(t)
                - COMM(t)
                - SURR_BEN(t)
                - MAT_BEN(t))


def PH_TAX_ON_PROFIT(t):

    """Shareholder tax payable on the profit"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return COB_PH(t) * Input.Tax_Rates["Policyholder"]


def POLS_DTH(t):

    """Number of death occurring at time t"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        flag = DUR_M(t) <= Input.surr_start_term["Surrender Start"]
        return IND_ACTIVE(t) * POLS_IF(t - 1) * MORT_RATE_MLY(t) * (flag + (1 - flag) * (1 - LAPSE_RATE_MLY(t)/2))


def POLS_IF(t):

    """Number of policies in-force

    Currently the model is for new business so the
    initial value is read from :func:`pols_if_init`.
    Subsequent values are defined recursively."""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    elif t == 0:
        return INIT_POLS_IF()
    else:
        return IND_ACTIVE(t) * (POLS_IF(t-1) - POLS_DTH(t) - POLS_LAPSE(t))


def POLS_LAPSE(t):

    """Number of lapse occurring at time t"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return IND_ACTIVE(t) * POLS_IF(t-1) * LAPSE_RATE_MLY(t) * (1 - MORT_RATE_MLY(t))


def POLS_MAT(t):

    """Number of maturing policies"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (DUR_M(t) == POL_TERM_M()) * POLS_IF(t)


def POL_TERM_M():

    """The policy term of the selected model point."""

    return POL_TERM_Y() * 12


def POL_TERM_Y():

    """The policy term of the selected model point.

    The element labeled ``policy_term`` of the Series returned by
    :func:`model_point`."""

    return MP()["policy_term"]


def PREM_PAYBL_M(t):

    """Monthly premium income
       Premium income during the period from ``t`` to ``t+1`` defined as::

       premium_pp(t)/premium frequency * pols_if(t)"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return IND_ACTIVE(t) * PREM_PP()/12 * POLS_IF(t-1)


def PREM_PP():

    """Annual premium per policy"""

    return MP()["ann_prem"]


def PREM_TERM_M():

    """Premium paying term in months"""

    return 12 * PREM_TERM_Y()


def PREM_TERM_Y():

    """Premium paying term in years"""

    return MP()["prem_paying_term"]


def PROFIT_AFT_TAX(t):

    """Profit after tax
    Profit after tax at ``t`` is defined as:

        profit_bef_tax(t) - sh_tax_on_profit(t) - ph_tax_on_profit(t)"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (PROFIT_BFR_TAX(t)
                - SH_TAX_ON_PROFIT(t)
                - PH_TAX_ON_PROFIT(t))


def PROFIT_AFT_TAX_AND_SH_TRNS(t):

    """Profit after tax and shareholder transfers
    Profit after tax and shareholder transfers at ``t`` is defined as:

        profit_aft_tax(t) - trns_sh(t) """

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return PROFIT_AFT_TAX(t) - TRNS_SH(t)


def PROFIT_AFT_TAX_SOLVM(t):

    """Profit after tax AND solvency margin"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (SH_TRNS_AFT_TAX(t)
                + INT_SOLVM(t)
                - INCR_SOLVM(t)
                - INV_EXP_SOLVM(t)
                - TAX_INT_SOLVM(t)) * (DUR_M(t) <= POL_TERM_M() + 1)


def PROFIT_BFR_TAX(t):

    """Profit before tax
    Profit before tax at ``t`` is defined as:
        (net_cf(t) - incr_reserve(t) + int_reserves(t))"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (DUR_M(t) <= POL_TERM_M() + 1) * (NET_CF(t) - INCR_RESERVE(t) + INT_RESERVES(t))


def PROJ_LEN():

    """Projection length in months

        defined as: Policy_Term - Duration(0) + 2"""

    return POL_TERM_M() - DUR_M(0) + 2


def PV_DB(t):

    """Present value of death benefit
    for the calculation of surrender value"""

    if t <= 0 or t > PROJ_LEN().max():
        return Input.pd.Series(0, index = MP().index)
    else:
        disc_fac = (1 + Input.yield_curve["Interest Rates"][Input.np.ceil(t/12)]) ** (1/12)
        mort1 = MORT_RATE_MLY(t)
        val = mort1 / disc_fac + PV_DB(t+1) * (1 - mort1)/disc_fac

        return IND_ACTIVE(t) * val


def PV_FP(t):

    """Present value of future profits"""

    if t < 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        disc_fac = 1 + DISC_RATE_M(t)
        return IND_ACTIVE(t) * (SH_TRNS_AFT_TAX(t+1) + PV_FP(t+1))/disc_fac


def PV_MAT_BEN(t):

    """Present Value of Maturity Benefit
    for the calculation of surrender value"""

    if t <= 0 or t > PROJ_LEN().max():
        return Input.pd.Series(0, index = MP().index)
    else:
        disc_fac = (1 + Input.yield_curve["Interest Rates"][Input.np.ceil(t/12)]) ** (1/12)
        mort1 = MORT_RATE_MLY(t)
        pv_mb = PV_MAT_BEN(t+1)/disc_fac

        return IND_ACTIVE(t) * pv_mb * (1 - mort1)  + (DUR_M(t) == POL_TERM_M() + 1)


def RESERVE_IF(t):

    """Reserve in-force:
        best estimate liability

    Reserve in-force at ``t`` is defined as:
        Max(reserve_pp(t), surr_val(t)) * pols_if(t)"""

    return POLS_IF(t) * RESERVE_PP_NET(t)


def RESERVE_PP(t):

    """Reserve per policy:
        best estimate liability

    Reserve per policy at ``t`` is defined as:
        max (0, Reserves.reserve_pp(t), SurrenderValue)"""

    return  Input.np.maximum(0, Input.np.maximum(SURR_VAL(t), Res.RESERVE_PP(t)))


def RESERVE_PP_NET(t):

    """Reserve per policy:
        best estimate liability"""

    return Input.np.maximum(RESERVE_PP(t), AS.AST_SHARE_END(t))


def SEX(): 

    """The sex of the selected model point(s)"""

    return MP()["sex"]


def SH_TAX_ON_PROFIT(t):

    """Shareholder tax payable on the profit"""

    if t < 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return PROFIT_BFR_TAX(t) * Input.Tax_Rates["Shareholder"]


def SH_TRNS_AFT_TAX(t):

    """Shareholder Transfers after Tax"""

    if t < 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return TRNS_SH(t) + (DUR_M(t) == POL_TERM_M() + 1) * ESTATE_ROLLUP(t) * Input.sh_prop["Share"]


def SOLVM_IF(t):

    """Solvency margin in-force

       Solvency margin in-force at 't' is defined as:
    """

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        ResPP = RESERVE_PP_NET(t) * Input.SM_Rates["% of Reserves"]

        pols_dth = Input.np.array([POLS_DTH(t)], dtype = float)
        dth_ben = Input.np.array([DTH_BEN(t)], dtype = float)
        dth_pay = Input.pd.Series(sum(Input.np.divide(dth_ben, pols_dth,out = Input.np.zeros_like(dth_ben), where = pols_dth!= 0)), index = MP().index)

        SAR = IND_ACTIVE(t) * Input.np.maximum(0, dth_pay - RESERVE_PP_NET(t)) * Input.SM_Rates["% of SAR"]

        return (ResPP + SAR) * Input.SM_Rates["Minimum Solvency Ratio"] * POLS_IF(t)


def SOLV_MARG_SH_FUNDED(t):

    """Solvency Margin Funded by Shareholder"""

    if t <= 0 or t > PROJ_LEN().max():
        return Input.pd.Series(0, index = MP().index)
    else:
        return IND_ACTIVE(t) * Input.np.maximum(0, SOLVM_IF(t) - Input.np.maximum(0, ESTATE_ROLLUP(t)))


def SSV(t):

    """Special Surrender Values
        Best Estimate basis"""

    return IND_ACTIVE(t) * (DUR_M(t) > Input.surr_start_term["Surrender Start"]) * (PV_DB(t) + PV_MAT_BEN(t)) * ((DUR_M(t)/(PREM_TERM_Y() * 12)) * SUM_ASSURED() + cob.DECLRD_REV_BONUS(t))


def SUM_ASSURED():

    """The sum assured of the selected model point(s)"""

    return MP()["sum_assured"]


def SURR_BEN(t):

    """Surrender Benefit"""

    return SURR_VAL(t) * POLS_LAPSE(t)


def SURR_TERM():

    """Term in months till which the surrender value is 0"""

    return Input.surr_start_term["Surrender Start"]


def SURR_VAL(t):

    """Surrender value
        defined as: Max(SSV, GSV)"""

    return Input.np.maximum(SSV(t), GSV(t)) * (DUR_M(t) >= SURR_TERM()) * IND_ACTIVE(t)


def TAX_INT_SOLVM(t):

    """Tax payable on interest earned on solvency margin

    This is defined as:
        max(Int_SolvM(t) - Inv_Exp_SolvM, 0) * ShareHolder_Tax"""

    return (DUR_M(t) <= POL_TERM_M()+1) * Input.np.maximum(INT_SOLVM(t) - INV_EXP_SOLVM(t), 0) * Input.Tax_Rates["Shareholder"]


def TRNS_SH(t):

    """Transfers to ShareHolders"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return COB_PH(t) * Input.sh_prop["Share"] / (1 - Input.sh_prop["Share"])


def VIF(t):

    """Value in force"""

    if t < 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        disc_fac = 1 + DISC_RATE_M(t)
        return (SOLV_MARG_SH_FUNDED(t+1) + PROFIT_AFT_TAX_SOLVM(t+1) + VIF(t+1))/disc_fac - SOLV_MARG_SH_FUNDED(t)


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("..", "Input"), "auto")

Res = ("Interface", ("..", "Reserves"), "auto")

cob = ("Interface", ("..", "COBFactor"), "auto")

AS = ("Interface", ("..", "AssetShare"), "auto")