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

def COMM(t):

    """Total commissions at time ``t``:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t) <= Proj.PREM_TERM_M()) * (COMM_INIT(t) + COMM_REN(t))


def COMM_INIT(t):

    """Initial Commission:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return COMM_RATE(t) * (1 + COMM_OVR_RATE(t)) * Proj.PREM_PP() * POLS_IF(t-1) * (Proj.DUR_M(t-1) == 0)


def COMM_OVR_RATE(t):

    """Commission override rates for projection:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.Commission.index.max()
        dur = list(Input.np.minimum(Proj.DUR_Y(t), n))
        comm_ovr = Input.Commission["Res Override"][dur]
        return Input.pd.Series(list(comm_ovr), index = Proj.MP().index)


def COMM_RATE(t):

    """Commission rates for Projection:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.Commission.index.max()
        dur = list(Input.np.minimum(Proj.DUR_Y(t), n))
        comm_rates = Input.Commission["Reserve"][dur]
        return Input.pd.Series(list(comm_rates), index = Proj.MP().index)


def COMM_REN(t):

    """Renewal Commission:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        flag = (Proj.DUR_M(t-1) > 0) * (Proj.DUR_M(t) <= Proj.PREM_TERM_M()) * ((Proj.DUR_M(t)-1)/12 == Proj.DUR_Y(t)-1)
        return COMM_RATE(t) * (1 + COMM_OVR_RATE(t)) * Proj.PREM_PP() * POLS_IF(t-1) * flag


def DTH_BEN(t):

    """Death benefit after probability:
        valuation basis"""    

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)        
    else:
        return DTH_BEN_AMT(t) * POLS_DTH(t) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def DTH_BEN_AMT(t):

    """Death benefit amount:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)        
    else:
        maxi = Input.np.maximum(Proj.SUM_ASSURED(t) - DTH_BEN_RED(t) + (Res_UF.AV_PP_AT(t,"BEF_PW_LB") + Res_UF.PW(t)) * Proj.IND_DB(),
                                DTH_BEN_MIN(t))
        return Input.np.maximum(maxi, Res_UF.AV_PP_AT(t, "BEF_PW_LB")+ Res_UF.PW(t)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def DTH_BEN_MIN(t):

    """Death benefit minimum:
        valuation basis

    Defined as Total Premiums Paid"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Input.np.minimum( Proj.DUR_Y(t), Proj.PREM_TERM_M()/12) * Proj.PREM_PP() * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def DTH_BEN_RED(t):

    """Death Benefit Reduction:
        valuation basis

    Based on the partial-withdrawal"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)        
    else:
        return (DTH_BEN_RED(t-1) + Res_UF.PW(t) - Res_UF.PW(t-24)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def EXPS(t):

    """Total expenses at time ``t``:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (EXP_INIT(t) + EXP_MAINT(t) + EXP_CLAIM(t)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def EXP_CLAIM(t):

    """Claim expenses:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)  
    else: 
        return Input.res_exp_claim["Claims"] * INFL_FAC(t-1)  * (POLS_DTH(t)+POLS_LAPSE(t)+POLS_MAT(t)) *(Proj.DUR_M(t)<= Proj.POL_TERM_M())


def EXP_INIT(t):

    """Initial Expenses:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        fixed = Input.res_exp_acq["Fixed"]
        prem_pc = Input.res_exp_acq["% of Premium"] * Proj.PREM_PP()
        sa_pc = Input.res_exp_acq["% of SA"] * Proj.SUM_ASSURED(t)
        return (fixed + prem_pc + sa_pc) * POLS_IF(t-1)* (Proj.DUR_M(t-1) == 0)


def EXP_MAINT(t):

    """Maintainance Expenses:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)  
    else: 
        fixed = Input.res_exp_maint["Fixed"] * INFL_FAC(t-1)/12
        prem_pc = Input.res_exp_maint["% of Premium"] * Proj.PREM_PP() * ((Proj.DUR_M(t)-1)/12 == Proj.DUR_Y(t)-1)
        res_pc = Res_UF.AV_PP_AT(t,"BEF_INV") * (1-(1- Input.res_exp_maint["% of Reserve"])** (1/12))
        return (fixed + prem_pc + res_pc)*POLS_IF(t-1)* (Proj.DUR_M(t-1)>0) *(Proj.DUR_M(t)<= Proj.POL_TERM_M())


def INFL_FAC(t):

    """The inflation factor at time ``t``:
        valuation basis"""

    if t < 0:
        raise ValueError("t cannot be less than 0.")
    else:
        return (1 + INFL_RATE()) ** (t/12)


def INFL_RATE():

    """Inflation rate:
        valuation basis"""

    return Input.res_infl_rate["Inflation"]


def LAPSE_RATE(t):

    """Lapse rate:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.Lapse.index.max()
        dur = list(Input.np.minimum(Proj.DUR_Y(t), n))
        rates = (list(Input.Lapse["Reserving"][dur]) * (Proj.DUR_M(t)/12 == Proj.DUR_Y(t)) * (Proj.DUR_M(t) <= Proj.PREM_TERM_M())
                 + list(1 - (1 - Input.Lapse["Reserving"][dur]) **(1/12)) * (Proj.DUR_M(t) > Proj.PREM_TERM_M()))* (Proj.DUR_M(t) <= Proj.POL_TERM_M())

        return rates


def MAT_BEN(t):

    """Maturity Benefit:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)        
    else:
        return Res_UF.AV_PP_AT(t-1, "END") * POLS_MAT(t) * (Proj.DUR_M(t-1) == Proj.POL_TERM_M())


def MORT_RATE_ANN(t):

    """Mortality rate to be applied at time ``t``:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        fac = Input.res_mort_scale["Male"] * (Proj.SEX() == 'M') + Input.res_mort_scale["Female"] * (Proj.SEX() == 'F')
        return fac * Input.BASE_MORT_RATE(t) * Proj.MP()["mort_loading"]


def MORT_RATE_MTH(t):

    """Monthly mortality rate to be applied at time ``t``:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return 1 - (1 - MORT_RATE_ANN(t)) ** (1/12)


def POLS_DTH(t):

    """Number of death occurring at time t:
        reserving"""

    if t <= 0:
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return POLS_IF(t - 1) *(1 - (0.5*LAPSE_RATE(t))) * MORT_RATE_MTH(t) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def POLS_IF(t):

    """Number of policies in-force:
        reserving

    Currently the model is for new business so the
    initial value is read from :func:`pols_if_init`.
    Subsequent values are defined recursively."""

    if t == 0:
        return Proj.INIT_POLS_IF()
    elif t < 0:
        raise ValueError("t cannot be less than 0.")
    else:
        return (Proj.DUR_M(t) <= Proj.POL_TERM_M()) * (POLS_IF(t-1) - POLS_DTH(t) - POLS_LAPSE(t))


def POLS_LAPSE(t):

    """Number of lapse occurring at time t:
        reserving"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return POLS_IF(t - 1) *(1-(MORT_RATE_MTH(t)/2)) *LAPSE_RATE(t) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def POLS_MAT(t):

    """Number of maturing policies:
        reserving

    The policy maturity occurs at ``t == 12 * policy_term()``,
    after death and lapse during the last period::

        pols_if(t-1) - pols_lapse(t-1) - pols_death(t-1)

    otherwise ``0``."""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Proj.DUR_M(t-1) == Proj.POL_TERM_M()) * POLS_IF(t-1)


def PREM_HOL_RATE(t):

    """Premium persistency rates used for projection:
        valuation basis"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        n = Input.PremHoliday["Reserving"].index.max()
        dur = list(Input.np.minimum(Proj.DUR_Y(t), n))
        return Input.pd.Series(list(Input.PremHoliday["Reserving"][dur]), index = Proj.MP().index)


def PREM_PAYBL_M(t):

    """Monthly premium income: reserving

       Premium income during the period from ``t`` to ``t+1`` defined as::

       premium_pp(t)/premium frequency * pols_if(t)"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Proj.PREM_PP() * PREM_HOL_RATE(t)* POLS_IF(t-1) * (Proj.DUR_M(t) <= Proj.PREM_TERM_M()) * ((Proj.DUR_M(t)-1)/12 == Proj.DUR_Y(t)-1)


def PW_PP(t):

    """Partial withdrawal per policy: reserving"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (Res_UF.PW(t) * POLS_IF(t-1)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def SERVICE_TAX(t):

    """Total service tax on all charges: reserving"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return ((Res_UF.ST_ALLOC(t) + Res_UF.ST_FMC(t) + Res_UF.ST_ADMIN(t) + Res_UF.ST_MORT(t)) * POLS_IF(t-1)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def SURR_BEN(t):

    """Surrender benefit: reserving"""

    if t <= 0:
        return Input.pd.Series( 0 , index = Proj.MP().index)
    else:
        n = Input.SurrCharge.index.max()
        surr_charge = Input.SURR_CHG_RATE(t) * Input.np.minimum(Proj.MP()["ann_prem"], Res_UF.AV_PP_AT(t, "BEF_PW_LB"))        
        return ((Res_UF.AV_PP_AT(t,"BEF_PW_LB") - Input.np.minimum(Input.SURR_CHG_CAP(t), surr_charge)) * POLS_LAPSE(t)) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def INT_NET_CF(t):

    """Interest on Net Cashflow"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        i = (1 + Input.res_IR["Reserve IR"]) ** (1/12) - 1
        return i * (PREM_PAYBL_M(t)
                    - MAT_BEN(t) 
                    - Res_UF.PREM_TO_AV_PP(t) * POLS_IF(t-1)
                    - EXPS(t)
                    - COMM(t)
                    - SERVICE_TAX(t)
                    + (Res_UF.CHG_ADMIN(t) + Res_UF.CHG_MORT(t)) * POLS_IF(t-1))


def UF_IF(t):

    """Unit Fund Inforce"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return Res_UF.AV_PP_AT(t, "BEF_PW_LB") * POLS_IF(t) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def INC_RES(t):

    """Increase in Reserves: reserving

    Defined as change in reserving unit fund at end"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (UF_IF(t) - UF_IF(t-1)) * (Proj.DUR_M(t) <= Proj.PROJ_LEN())


def INT_RES(t):

    """Interest on Reserves: reserving"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        inv_rate = (1 + Input.res_UF_FMC["Unit Growth"]) ** (1/12) - 1
        return Res_UF.AV_PP_AT(t, "BEF_INV") * inv_rate *  POLS_IF(t-1) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


def NET_CF(t):

    """Net Cashflow: reserving"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        return (PREM_PAYBL_M(t)
                    + INT_NET_CF(t) 
                    + INT_RES(t)
                    - DTH_BEN(t) 
                    - SURR_BEN(t) 
                    - PW_PP(t) 
                    - MAT_BEN(t) 
                    - EXPS(t)
                    - COMM(t)
                    - SERVICE_TAX(t)
                    - INC_RES(t)) * (Proj.DUR_M(t) <= Proj.PROJ_LEN())


def NLR_IF(t):

    """Non Linked Reserve Inforce"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        flag = (Proj.DUR_M(t) > 0) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())
        return flag * Input.np.maximum(NLR_IF(t+1) - NET_CF(t+1), 0) / ((1 + Input.res_IR["Reserve IR"]) ** (1/12))


def NLR_PP(t):

    """Non Linked Reserve Per Policy"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        pols = Input.np.array([POLS_IF(t)], dtype = float)
        nlr = Input.np.array([NLR_IF(t)], dtype = float)
        nlr_pp = Input.np.divide(nlr, pols, out = Input.np.zeros_like(nlr), where = pols != 0)

        return Input.pd.Series(sum(nlr_pp), index = Proj.MP().index)


def UPR(t):

    """Unearned premium reserves"""

    if t <= 0 or t > Proj.MAX_PROJ_LEN():
        return Input.pd.Series(0, index = Proj.MP().index)
    else:
        mort= Input.CHG_MORT_RATE(t-1) * Proj.MP()["mort_loading"]
        scale = Input.res_mort_chg_pc["Male"] * (Proj.SEX() == "M") + Input.res_mort_chg_pc["Female"] * (Proj.SEX() == "F")
        return ((UF.SAR(t)* mort * scale) / 12) * (Proj.DUR_M(t) <= Proj.POL_TERM_M())


# ---------------------------------------------------------------------------
# References

Input = ("Interface", ("..", "Input"), "auto")

UF = ("Interface", ("..", "Unit_Fund"), "auto")

Proj = ("Interface", ("..", "Projection"), "auto")

Proj_DPF = ("Interface", ("..", "Projection_DPF"), "auto")

Res_UF = ("Interface", ("..", "Reserve_UF"), "auto")