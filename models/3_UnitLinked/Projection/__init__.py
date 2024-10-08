"""The main Space in the :mod:`~savings.CashValue_ME` model.

:mod:`~savings.CashValue_ME.Projection` is the only Space defined
in the :mod:`~savings.CashValue_ME` model, and it contains
all the logic and data used in the model.

.. rubric:: Parameters and References

(In all the sample code below,
the global variable ``Projection`` refers to the
:mod:`~savings.CashValue_ME.Projection` Space.)

Attributes:

    model_point_table: All model points as a DataFrame.
        By default, 4 model points are defined.
        The DataFrame has an index named ``point_id``.

            * ``spec_id``
            * ``age_at_entry``
            * ``sex``
            * ``policy_term``
            * ``policy_count``
            * ``sum_assured``
            * ``duration_mth``
            * ``premium_pp``
            * ``av_pp_init``

        Cells defined in :mod:`~savings.CashValue_ME.Projection`
        with the same names as these columns return
        the corresponding column's values for the selected model point.

        .. code-block::

            >>> Projection.model_poit_table
                     spec_id  age_at_entry sex  ...  premium_pp  av_pp_init
            poind_id                            ...
            1              A            20   M  ...      500000           0
            2              B            50   M  ...      500000           0
            3              C            20   M  ...        1000           0
            4              D            50   M  ...        1000           0

            [4 rows x 10 columns]

        The DataFrame is saved in the Excel file *model_point_samples.xlsx*
        placed in the model folder.
        :attr:`model_point_table` is created by
        Projection's `new_pandas`_ method,
        so that the DataFrame is saved in the separate file.
        The DataFrame has the injected attribute
        of ``_mx_dataclident``::

            >>> Projection.model_point_table._mx_dataclient
            <PandasData path='model_point_table_samples.xlsx' filetype='excel'>

        .. seealso::

           * :func:`model_point`
           * :func:`age_at_entry`
           * :func:`sex`
           * :func:`policy_term`
           * :func:`pols_if_init`
           * :func:`sum_assured`
           * :func:`duration_mth`
           * :func:`premium_pp`
           * :func:`av_pp_init`

    model_point_10000: Alternative model point table

        This model point table contains 10000 model points and
        is saved as the Excel file *model_point_10000.xlsx*
        placed in the folder. To use this table, assign it to
        :attr:`model_point_table`::

            >>> Projection.model_point_table = Projection.model_point_10000


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

    std_norm_rand: Random numbers drawn from the standard normal distribution

        A Series of random numbers drawn from the standard normal distribution
        indexed with ``scen_id`` and ``t``.
        Used for generating investment returns. See :func:`inv_return_table`.

    scen_id: Selected scenario ID

        An integer indicating the selected scenario ID.
        :attr:`scen_id` is referenced in by :func:`inv_return_mth`
        as one of the keys to select a scenario from :attr:`std_norm_rand`.

    surr_charge_table: Surrender charge rates by duration

        A DataFrame of multiple patterns of surrender charge rates by duration.
        The column labels indicate :func:`surr_charge_id`.
        By default, ``"type_1"``, ``"type_2"`` and ``"type_3"`` are defined.

    product_spec_table: Table of product specs

        A DataFrame of product spec parameters by ``spec_id``.
        :attr:`model_point_table` and :attr:`product_spec_table` columns
        are joined in :func:`model_point_table_ext`,
        and the :attr:`product_spec_table` columns become part
        of the model point attributes.
        The :attr:`product_spec_table` columns are read
        by the Cells with the same names as the columns:

        * :func:`premium_type`
        * :func:`has_surr_charge`
        * :func:`surr_charge_id`
        * :func:`load_prem_rate`
        * :func:`is_wl`

        .. code-block::

            >>> Projection.product_spec_table
                    premium_type  has_surr_charge surr_charge_id  load_prem_rate  is_wl
            spec_id
            A             SINGLE            False            NaN            0.10  False
            B             SINGLE             True         type_1            0.00  False
            C              LEVEL            False            NaN            0.10   True
            D              LEVEL             True         type_3            0.05   True


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

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def AGE(t):

    """The attained age at time t.

        age_at_entry() + dur_y(t+1)
    """

    return AGE_AT_ENTRY() + DUR_Y(t+1) - 1


def AGE_AT_ENTRY():

    """The age at entry of the model points

    The ``age_at_entry`` column of the DataFrame returned by
    :func:`model_point`.
    """

    return MP()["age_at_entry"]


def COMM(t):

    """Total commissions at time t"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (COMM_INIT(t) + COMM_REN(t) + Proj_DPF.COMM(t)) * (DUR_M(t) <= PREM_TERM_M())


def COMM_CLAWBACK(t):

    """Clawback Commission"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        claw = PREM_PP() * DUR_Y(t) * Input.CLAWBACK_RATE(t) * Input.claw_ind["Clawback Ind"] * COMM_RATE(1) * (1 + COMM_OVR_RATE(1))
        return - claw * POLS_LAPSE(t) * (DUR_M(t) <= Input.claw_mth["Clawback Month"])


def COMM_INIT(t):

    """Initial Commission"""

    if t <= 0 or t > MAX_PROJ_LEN():
       return Input.pd.Series(0, index = MP().index)
    else:
        return COMM_RATE(t) * (1+ COMM_OVR_RATE(t)) * PREM_PP() * POLS_IF(t-1) * (DUR_M(t-1)==0)


def COMM_OVR_RATE(t):

    """Commission override rates for Projection"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        n = Input.Commission.index.max()
        dur = list(Input.np.minimum(DUR_Y(t), n))
        comm_ovr = Input.Commission["Proj Override"][dur]
        return Input.pd.Series(list(comm_ovr), index = MP().index)


def COMM_RATE(t):

    """Commission rates for Projection"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        n = Input.Commission.index.max()
        dur = list(Input.np.minimum(DUR_Y(t), n))
        comm_rates = Input.Commission["Projection"][dur]
        return Input.pd.Series(list(comm_rates), index = MP().index)


def COMM_REN(t):

    """Renewal Commission"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return COMM_RATE(t) * (1+COMM_OVR_RATE(t)) * PREM_PP() * POLS_IF(t-1) * (DUR_M(t-1)>0) * (DUR_M(t) <= PREM_TERM_M()) * ((DUR_M(t)-1)/12 == DUR_Y(t)-1)


def DPF_PP(t):

    """DPF Outgo"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return Proj_DPF.MAT_BEN(t) * (DUR_M(t) <= POL_TERM_M())


def DTH_BEN(t):

    """Death Benefit after probability"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        return DTH_BEN_AMT(t) * POLS_DTH(t) * IND_ACTIVE(t) + Proj_DPF.DTH_BEN(t)


def DTH_BEN_AMT(t):

    """Death benefit amount before probability"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        maxi = Input.np.maximum(SUM_ASSURED(t) - DTH_BEN_RED(t) + UF.AV_PP_AT(t, "BEF_PW_LB") * IND_DB(),
                                DTH_BEN_MIN(t))

        return Input.np.maximum(maxi, UF.AV_PP_AT(t, "BEF_PW_LB")) * IND_ACTIVE(t)


def DTH_BEN_MIN(t):

    """Death benefit minimum:
        defined as TotalPremiumsPaid"""

    return Input.np.minimum(DUR_Y(t), PREM_TERM_M()/12) * PREM_PP() * (DUR_M(t) <= POL_TERM_M())


def DTH_BEN_RED(t):

    """Death Benefit Reduction:
        best estimate basis

    Based on the partial-withdrawal
    """

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        return (DTH_BEN_RED(t-1) + UF.PW(t) - UF.PW(t-24)) * (DUR_M(t) <= POL_TERM_M())


def DUR_M(t):

    """Duration of model points at ``t`` in months"""

    if t < 0:
        raise ValueError("t cannot be less than 0")
    elif t == 0:
        return MP()['dur_elapsed']
    else:
        return DUR_M(t-1) + 1


def DUR_Y(t):

    """Duration of model points at ``t`` in years
    """

    return Input.pd.Series(list((DUR_M(t)/12).apply(Input.np.ceil)), index = MP().index)


def EXPS(t):

    """Total expenses at time ``t``"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return EXP_INIT(t) + EXP_MAINT(t) + EXP_CLAIM(t)


def EXP_CLAIM(t):

    """Claim expenses"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)  
    else: 
        return (Input.exp_claim["Claims"] * INFL_FAC(t-1) * (POLS_DTH(t) + POLS_LAPSE(t) + POLS_MAT(t))
                + Proj_DPF.EXP_CLAIM(t)) * (DUR_M(t-1) <= POL_TERM_M())


def EXP_INIT(t):

    """Initial Expenses"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series( 0, index = MP().index)
    else:
        fixed = Input.exp_acq["Fixed"]
        prem_pc = Input.exp_acq["% of Premium"] * PREM_PP()
        sa_pc = Input.exp_acq["% of SA"] * SUM_ASSURED(t)

        return (fixed + prem_pc + sa_pc) * POLS_IF(t-1) * (DUR_M(t-1)==0)


def EXP_MAINT(t):

    """Maintainance Expenses"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)  
    else: 
        fixed = Input.exp_maint["Fixed"] * INFL_FAC(t-1)/12
        prem_pc = Input.exp_maint["% of Premium"] * PREM_PAYBL_M(t) * (DUR_M(t) <= POL_TERM_M()) * ((DUR_M(t)-1)/12 == DUR_Y(t) - 1)
        res_pc = (UF.AV_PP_AT(t, "BEF_INV") + NLR_PP(t-1)) * (1 - (1 - Input.exp_maint["% of Reserve"]) ** (1/12))

        return ((fixed + prem_pc + res_pc) * POLS_IF(t-1) + Proj_DPF.EXP_MAINT(t)) * (DUR_M(t-1) > 0) * (DUR_M(t) <= POL_TERM_M())


def INCR_RES(t):

    """Increase in reserves"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index= MP().index)
    else:
        return UF_IF(t) + NLR_IF(t) - UF_IF(t-1) - NLR_IF(t-1)


def INCR_SOLVM(t):

    """Increase in solvency margin"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index=MP().index)
    else:
        return SOLVM_IF(t) - SOLVM_IF(t-1)


def IND_ACTIVE(t):

    """Indicator if the policy is active"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    elif t == 0:
        return Input.pd.Series(1, index = MP().index)
    else:
        return (DUR_M(t) <= POL_TERM_M()) * (POLS_IF(t-1) > 0)


def IND_DB():

    """Death Benefit Option Indicator

        0: Maxiumum(Sum Assured, Unit Fund)
        1: Sum (Sum Assured, Unit Fund)
    """

    return MP()["death_benefit_option"]


def INFL_FAC(t):

    """The inflation factor at time t"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    else:
        return (1 + INFL_RATE()) ** (t/12)


def INFL_RATE():

    """Inflation rate

    The inflation rate to be applied to the expense assumption.
    By defualt it is set to ``0.01``.

    .. seealso::

        * :func:`inflation_factor`

    """

    return Input.infl_rate["Inflation"]


def INIT_POLS_IF(): 

    """Initial Number of Policies In-force

    Number of in-force policies at time 0 referenced from :func:`pols_if`.
    Defaults to 1."""

    return Input.pd.Series(1, index = MP().index)


def INT_NET_CF(t):

    """Interest earned on net cashflows"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        y = Input.np.ceil(t/12)
        i = (1 + Input.YieldCurve["Non-Unit Interest Rates"][y]) ** (1/12) - 1
        return i * (PREM_PAYBL_M(t)
                    - UF.PREM_TO_AV_PP(t) * POLS_IF(t-1)
                    - EXP_INIT(t)
                    - EXP_MAINT(t)
                    - COMM(t)
                    + COMM_CLAWBACK(t)
                    + (UF.CHG_ADMIN(t) + UF.CHG_MORT(t)) * POLS_IF(t-1))


def INT_RES(t):

    """Interest earned on reserves"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        y = Input.np.ceil(t/12)
        i_unit = (1 + Input.YieldCurve["Unit Interest Rates"][y]) ** (1/12) - 1
        i_n_unit = (1 + Input.YieldCurve["Non-Unit Interest Rates"][y]) ** (1/12) - 1

        u_int =  i_unit * (UF.AV_PP_AT(t, "BEF_INV") * POLS_IF(t-1)
                           + UF_DPF.AV_PP_AT(t,"BEF_INV") * Proj_DPF.POLS_IF(t-1))

        return (u_int + (NLR_IF(t-1) * i_n_unit)) * (DUR_M(t) <= PROJ_LEN())


def INT_SOLVM(t):

    """Interest earned on solvency margin"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        y = Input.np.ceil(t/12)
        i = (1 + Input.YieldCurve["Non-Unit Interest Rates"][y]) ** (1/12) - 1
        return SOLVM_IF(t-1) * i


def INV_EXP_SOLVM(t):

    """Investment expenses on solvency margin"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        y = Input.np.ceil((t)/12)
        i = (1 + Input.YieldCurve["Non-Unit Interest Rates"][y]) ** (1/12) - 1
        i_exp = (1 + Input.YieldCurve["Non-Unit Interest Rates"][y] - Input.exp_maint["% of Reserve"]) ** (1/12) - 1
        return SOLVM_IF(t-1) * (i - i_exp)


def LAPSE_RATE(t):

    """Lapse rate"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        n = Input.Lapse.index.max()
        dur = list(Input.np.minimum(DUR_Y(t), n))
        rates = (list(Input.Lapse["Projection"][dur]) * (DUR_M(t)/12 == DUR_Y(t)) * (DUR_M(t) <= PREM_TERM_M()) + 
                list(1 - (1 - Input.Lapse["Projection"][dur]) **(1/12)) * (DUR_M(t) > PREM_TERM_M()))

        return rates


def MAT_BEN(t):

    """ Maturity Benefit"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        return UF.AV_PP_AT(t-1, "END") * POLS_MAT(t) * (DUR_M(t-1) == POL_TERM_M())


MAX_PROJ_LEN = lambda: PROJ_LEN().max()
"""The max of all projection lengths

Defined as ``max(proj_len())``

.. seealso::
    :func:`proj_len`
"""

def MORT_RATE_ANN(t):

    """Mortality rate to be applied at time t"""

    fac = Input.mort_scale["Male"] * (SEX() == 'M') + Input.mort_scale["Female"] * (SEX() == 'F')
    return fac * Input.BASE_MORT_RATE(t) * MP()["mort_loading"]


def MORT_RATE_MTH(t):

    """Monthly mortality rate to be applied at time ``t``"""

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
        raise ValueError(f"Incompatible data type for Input.point_id: {type(Input.point_id)}")


def NLR_IF(t):

    """Non linked reserve per policy"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return NLR_PP(t) * POLS_IF(t)


def NLR_PP(t):

    """Non linked reserve per policy"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return Input.np.maximum(0, Input.np.maximum(Res.NLR_PP(t), Res.UPR(t)))


def POLS_DTH(t):

    """Number of death occurring at time t"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        lapse = LAPSE_RATE(t) * (0.5 * (DUR_M(t) >= Input.surr_mth["Surrender Month"]))
        rates = POLS_IF(t - 1) * MORT_RATE_MTH(t) * (1 - lapse) * (DUR_M(t) <= POL_TERM_M())
        rates2 = POLS_IF(t - 1) * MORT_RATE_MTH(t) * (DUR_M(t) <= POL_TERM_M())

        return rates * (UF.AV_PP_AT(t, "BEF_PW_LB") > 0) + rates2 * (UF.AV_PP_AT(t, "BEF_PW_LB") <= 0)


def POLS_IF(t):

    """Number of policies in-force
    Subsequent values are defined recursively."""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    elif t == 0:
        return INIT_POLS_IF()
    else:
        return (DUR_M(t) <= POL_TERM_M()) * (POLS_IF(t-1) - POLS_DTH(t) - POLS_LAPSE(t))


def POLS_LAPSE(t):

    """Number of lapse occurring at time t"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        death  = MORT_RATE_MTH(t) * (1 - (0.5 * (DUR_M(t) > Input.surr_mth["Surrender Month"])))
        rates  = POLS_IF(t-1) * (1 - death) * LAPSE_RATE(t) * (DUR_M(t) <= POL_TERM_M())
        rates2 = (POLS_IF(t-1) - POLS_DTH(t)) * (DUR_M(t) <= POL_TERM_M())

        return rates * (UF.AV_PP_AT(t, "BEF_PW_LB") > 0) + rates2 * (UF.AV_PP_AT(t, "BEF_PW_LB") <= 0)


def POLS_MAT(t):

    """Number of maturing policies

    The policy maturity occurs at ``t == 12 * policy_term()``,
    after death and lapse during the last period::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)

    otherwise ``0``."""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        return (DUR_M(t-1) == POL_TERM_M()) * POLS_IF(t-1)


def POL_TERM_M():

    """The policy term of the model points in months.

    The ``policy_term`` column of the DataFrame returned by
    :func:`model_point`.
    """

    return POL_TERM_Y() * 12


def POL_TERM_Y():

    """The policy term of the model points.

    The ``policy_term`` column of the DataFrame returned by
    :func:`model_point`.
    """

    return MP()["policy_term"]


def PREM_HOL_RATE(t):

    """Premium persistency rates used for projection"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        n = Input.PremHoliday["Projection"].index.max()
        dur = list(Input.np.minimum(DUR_Y(t), n))
        return Input.pd.Series(list(Input.PremHoliday["Projection"][dur]), index = MP().index)


def PREM_PAYBL_M(t):

    """Monthly premium income

       Premium income during the period from ``t`` to ``t+1`` defined as::

       premium_pp(t)/premium frequency * pols_if(t)"""

    if t <= 0:
        return Input.pd.Series(0, index = MP().index)
    else:
        return PREM_PP() * PREM_HOL_RATE(t)* POLS_IF(t-1) * (DUR_M(t) <= PREM_TERM_M()) * ((DUR_M(t)-1)/12 == DUR_Y(t)-1)


def PREM_PP():

    """Premium amount per policy.

    Annual level premium if :func:`PREM_TYPE` is `LEVEL` 
    """

    return MP()["ann_prem"]


def PREM_TERM_M():

    """Premium Paying Term"""

    return MP()["prem_paying_term"] * 12


def PREM_TYPE():

    """Type of premium payment

    Returns a string indicating the payment type, which is either
    ``"LEVEL"`` if level payment, or ``"SINGLE"`` if single payment."""

    return MP()['premium_type']


def PROJ_LEN():

    """Projection length in months

    :func:`proj_len` returns how many months the projection
    for each model point should be carried out
    for all the model point. Defined as::

        np.maximum(12 * policy_term() - duration_mth(0) + 2, 0)

    Since this model carries out projections for all the model points
    simultaneously, the projections are actually carried out
    from 0 to :func:`MAX_PROJ_LEN` for all the model points.
    """

    return Input.np.maximum(POL_TERM_M() - DUR_M(0) + 2, 0)


def PRO_AFT_SM(t):

    """Profit after solvency margin"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return (PRO_AFT_TAX(t)
                + INT_SOLVM(t) 
                - INCR_SOLVM(t)
                - INV_EXP_SOLVM(t)
                - TAX_INT_SM(t))


def PRO_AFT_TAX(t):

    """Profit after tax"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index= MP().index)
    else:
        return PRO_BEF_TAX(t) - TAX_PRO(t)


def PRO_BEF_TAX(t):

    """Profit before tax and solvency margin"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
       return (PREM_PAYBL_M(t)
              + INT_NET_CF(t)
              + INT_RES(t)
              - INCR_RES(t)
              - DTH_BEN(t)
              - SURR_BEN(t)
              - PW_PP(t)
              - MAT_BEN(t)
              - DPF_PP(t)
              - EXPS(t)
              - COMM(t)
              - COMM_CLAWBACK(t)
              - SERVICE_TAX(t))


def PVFP(t):

    """Present Value of Future Profits"""

    if t < 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index= MP().index)
    else:
        n = Input.YieldCurve.index.max()
        y = Input.np.minimum(Input.np.ceil((t+1)/12), n)
        i = (1 + Input.YieldCurve["Discount Rates"][y]) ** (1/12)
        return (PVFP(t+1) + PRO_AFT_TAX(t+1))/i * (DUR_M(t) <= POL_TERM_M())


def PW_PP(t):

    """Partial withdrawal per policy"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return UF.PW(t) * POLS_IF(t)


def PW_RATES(t):

    """Partial Withdrawal Rates"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)        
    else:
        n = Input.PartialWithdrawal["Projection"].index.max()
        dur = list(Input.np.minimum(DUR_Y(t), n))
        return Input.pd.Series(list(Input.PartialWithdrawal["Projection"][dur]), index = MP().index)


def SERVICE_TAX(t):

    """Total service tax on all charges"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index=MP().index)
    else:
        tax = (UF.ST_ADMIN(t)
              + UF.ST_ALLOC(t)
              + UF.ST_MORT(t)
              + UF.ST_FMC(t))

        return tax * POLS_IF(t-1) * IND_ACTIVE(t) + Proj_DPF.SERVICE_TAX(t)


def SEX():

    """The sex of the model points"""

    return MP()["sex"]


def SOLVM_IF(t):

    """Solvency margin in-force"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index=MP().index)
    else:
        res = (UF.AV_PP_AT(t, "BEF_PW_LB") + NLR_PP(t)) * Input.SM_Rates["% of Reserves"] * Input.SM_Rates["Minimum Solvency Ratio"]
        sar = Input.np.maximum(DTH_BEN_AMT(t) - NLR_PP(t) - UF.AV_PP_AT(t, "BEF_PW_LB") * (1 - IND_DB()), 0) * Input.SM_Rates["% of SAR"] * Input.SM_Rates["Minimum Solvency Ratio"]
        return (res + sar) * (UF.AV_PP_AT(t, "BEF_PW_LB") > 0) * POLS_IF(t) * IND_ACTIVE(t) + Proj_DPF.SOLVM_IF(t)


def SUM_ASSURED(t):

    """The sum assured of the model points

    This is defined as:
        max(Sum_assured, MinDBFactor * TotalPremiumsPaid)
    """

    return Input.np.maximum(MP()['sum_assured'], Input.min_DB["Min DB"] * (Input.np.minimum(DUR_Y(t), PREM_TERM_M()/12) * PREM_PP())) * (DUR_M(t) <= POL_TERM_M())


def SURR_BEN(t):

    """Surrender benefit"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0 , index = MP().index)
    else:
        return (UF.AV_PP_AT(t,"BEF_PW_LB") * POLS_LAPSE(t) * (DUR_M(t) >= Input.surr_mth["Surrender Month"])) * IND_ACTIVE(t)


def TAX_INT_SM(t):

    """Tax on interest earned on solvency margin"""

    return Input.np.maximum(0, (INT_SOLVM(t) - INV_EXP_SOLVM(t)) * Input.tax_rates["Shareholder"])


def TAX_PRO(t):

    """Tax on profit"""    

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index= MP().index)
    else:
        return Input.np.maximum(0, PRO_BEF_TAX(t) * Input.tax_rates["Shareholder"])


def UF_IF(t):

    """Unit fund per policy inforce"""

    if t <= 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index = MP().index)
    else:
        return UF.AV_PP_AT(t, "BEF_PW_LB") * POLS_IF(t) * IND_ACTIVE(t) + Proj_DPF.UF_IF(t)


def VIF(t):

    """Value in-force"""

    if t < 0 or t > MAX_PROJ_LEN():
        return Input.pd.Series(0, index= MP().index)
    else:
        n = Input.YieldCurve.index.max()
        y = Input.np.minimum(Input.np.ceil((t+1)/12), n)
        disc_fac = (1 + Input.YieldCurve["Discount Rates"][y]) ** (1/12)
        return (VIF(t+1) + PRO_AFT_SM(t+1) + SOLVM_IF(t+1)) / disc_fac * (DUR_M(t) <= POL_TERM_M()) - SOLVM_IF(t)


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("..", "Input"), "auto")

UF = ("Interface", ("..", "Unit_Fund"), "auto")

Proj_DPF = ("Interface", ("..", "Projection_DPF"), "auto")

Res = ("Interface", ("..", "Reserve"), "auto")

UF_DPF = ("Interface", ("..", "Unit_Fund_DPF"), "auto")