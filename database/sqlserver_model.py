from sqlalchemy import Column, DateTime
from sqlalchemy import Float, String, BigInteger, Index
from sqlalchemy.ext.declarative import declarative_base

from database.model import MetaMixin

Base = declarative_base()


class BattleLog(Base, MetaMixin):
    __tablename__ = 'BattleLog'
    # __abstract__ = True
    id = Column(String(50), primary_key=True)
    timestamp_ended = Column(BigInteger)
    attacker_id = Column(String(50))
    attacker_faction = Column(String(50))
    attacker_name = Column(String(50))
    attacker_factionname = Column(String(50))
    defender_id = Column(String(50))
    defender_faction = Column(String(50))
    defender_name = Column(String(50))
    defender_factionname = Column(String(50))
    respect_gain = Column(Float)
    result = Column('result', String(50), )
    chain = Column(BigInteger)
    ff = Column(Float, default=0)
    war = Column(Float, default=0)
    retaliation = Column(Float, default=0)
    group_attack = Column(Float, default=0)
    overseas = Column(Float, default=0)
    chain_bonus = Column(Float, default=0)


class TornBingWaAllData(Base, MetaMixin):
    __tablename__ = 'TornBingWaAllData'
    TransDate = Column(String(30), primary_key=True)
    player_id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    estimate_bs = Column(BigInteger, default=0, nullable=False)
    estimate_bs_display = Column(String(200), default='', nullable=False)
    faction_id_faction = Column(BigInteger, default=0, nullable=False)
    faction_name_faction = Column(String(100))
    company_id_job = Column(BigInteger, default=0, nullable=False)
    company_name_job = Column(String(100))
    spouse_id_married = Column(BigInteger, default=0, nullable=False)
    spouse_name_married = Column(String(100))
    level = Column(BigInteger, default=0, nullable=False)
    property = Column(String(100))
    virusescoded_personalstats = Column(BigInteger, default=0, nullable=False)
    attackswon_personalstats = Column(BigInteger, default=0, nullable=False)
    attackslost_personalstats = Column(BigInteger, default=0, nullable=False)
    attacksdraw_personalstats = Column(BigInteger, default=0, nullable=False)
    attacksassisted_personalstats = Column(BigInteger, default=0, nullable=False)
    defendswon_personalstats = Column(BigInteger, default=0, nullable=False)
    defendslost_personalstats = Column(BigInteger, default=0, nullable=False)
    defendsstalemated_personalstats = Column(BigInteger, default=0, nullable=False)
    defendslostabroad_personalstats = Column(BigInteger, default=0, nullable=False)
    moneymugged_personalstats = Column(BigInteger, default=0, nullable=False)
    largestmug_personalstats = Column(BigInteger, default=0, nullable=False)
    itemsbought_personalstats = Column(BigInteger, default=0, nullable=False)
    auctionswon_personalstats = Column(BigInteger, default=0, nullable=False)
    auctionsells_personalstats = Column(BigInteger, default=0, nullable=False)
    cityitemsbought_personalstats = Column(BigInteger, default=0, nullable=False)
    pointsbought_personalstats = Column(BigInteger, default=0, nullable=False)
    jailed_personalstats = Column(BigInteger, default=0, nullable=False)
    peoplebusted_personalstats = Column(BigInteger, default=0, nullable=False)
    failedbusts_personalstats = Column(BigInteger, default=0, nullable=False)
    peoplebought_personalstats = Column(BigInteger, default=0, nullable=False)
    peopleboughtspent_personalstats = Column(BigInteger, default=0, nullable=False)
    hospital_personalstats = Column(BigInteger, default=0, nullable=False)
    medicalitemsused_personalstats = Column(BigInteger, default=0, nullable=False)
    bloodwithdrawn_personalstats = Column(BigInteger, default=0, nullable=False)
    revives_personalstats = Column(BigInteger, default=0, nullable=False)
    revivesreceived_personalstats = Column(BigInteger, default=0, nullable=False)
    selling_illegal_products_criminalrecord = Column(BigInteger, default=0, nullable=False)
    theft_criminalrecord = Column(BigInteger, default=0, nullable=False)
    auto_theft_criminalrecord = Column(BigInteger, default=0, nullable=False)
    drug_deals_criminalrecord = Column(BigInteger, default=0, nullable=False)
    computer_crimes_criminalrecord = Column(BigInteger, default=0, nullable=False)
    fraud_crimes_criminalrecord = Column(BigInteger, default=0, nullable=False)
    murder_criminalrecord = Column(BigInteger, default=0, nullable=False)
    other_criminalrecord = Column(BigInteger, default=0, nullable=False)
    organisedcrimes_personalstats = Column(BigInteger, default=0, nullable=False)
    bountiesplaced_personalstats = Column(BigInteger, default=0, nullable=False)
    totalbountyspent_personalstats = Column(BigInteger, default=0, nullable=False)
    bountiescollected_personalstats = Column(BigInteger, default=0, nullable=False)
    totalbountyreward_personalstats = Column(BigInteger, default=0, nullable=False)
    bountiesreceived_personalstats = Column(BigInteger, default=0, nullable=False)
    receivedbountyvalue_personalstats = Column(BigInteger, default=0, nullable=False)
    cityfinds_personalstats = Column(BigInteger, default=0, nullable=False)
    itemsdumped_personalstats = Column(BigInteger, default=0, nullable=False)
    dumpfinds_personalstats = Column(BigInteger, default=0, nullable=False)
    booksread_personalstats = Column(BigInteger, default=0, nullable=False)
    boostersused_personalstats = Column(BigInteger, default=0, nullable=False)
    consumablesused_personalstats = Column(BigInteger, default=0, nullable=False)
    candyused_personalstats = Column(BigInteger, default=0, nullable=False)
    alcoholused_personalstats = Column(BigInteger, default=0, nullable=False)
    energydrinkused_personalstats = Column(BigInteger, default=0, nullable=False)
    argtravel_personalstats = Column(BigInteger, default=0, nullable=False)
    cantravel_personalstats = Column(BigInteger, default=0, nullable=False)
    caytravel_personalstats = Column(BigInteger, default=0, nullable=False)
    chitravel_personalstats = Column(BigInteger, default=0, nullable=False)
    dubtravel_personalstats = Column(BigInteger, default=0, nullable=False)
    hawtravel_personalstats = Column(BigInteger, default=0, nullable=False)
    japtravel_personalstats = Column(BigInteger, default=0, nullable=False)
    lontravel_personalstats = Column(BigInteger, default=0, nullable=False)
    mextravel_personalstats = Column(BigInteger, default=0, nullable=False)
    soutravel_personalstats = Column(BigInteger, default=0, nullable=False)
    switravel_personalstats = Column(BigInteger, default=0, nullable=False)
    rehabcost_personalstats = Column(BigInteger, default=0, nullable=False)
    rehabs_personalstats = Column(BigInteger, default=0, nullable=False)
    overdosed_personalstats = Column(BigInteger, default=0, nullable=False)
    victaken_personalstats = Column(BigInteger, default=0, nullable=False)
    xantaken_personalstats = Column(BigInteger, default=0, nullable=False)
    cantaken_personalstats = Column(BigInteger, default=0, nullable=False)
    exttaken_personalstats = Column(BigInteger, default=0, nullable=False)
    kettaken_personalstats = Column(BigInteger, default=0, nullable=False)
    lsdtaken_personalstats = Column(BigInteger, default=0, nullable=False)
    opitaken_personalstats = Column(BigInteger, default=0, nullable=False)
    pcptaken_personalstats = Column(BigInteger, default=0, nullable=False)
    shrtaken_personalstats = Column(BigInteger, default=0, nullable=False)
    spetaken_personalstats = Column(BigInteger, default=0, nullable=False)
    missioncreditsearned_personalstats = Column(BigInteger, default=0, nullable=False)
    missionscompleted_personalstats = Column(BigInteger, default=0, nullable=False)
    contractscompleted_personalstats = Column(BigInteger, default=0, nullable=False)
    dukecontractscompleted_personalstats = Column(BigInteger, default=0, nullable=False)
    racesentered_personalstats = Column(BigInteger, default=0, nullable=False)
    raceswon_personalstats = Column(BigInteger, default=0, nullable=False)
    racingpointsearned_personalstats = Column(BigInteger, default=0, nullable=False)
    networth_personalstats = Column(BigInteger, default=0, nullable=False)
    awards = Column(BigInteger, default=0, nullable=False)
    nerverefills_personalstats = Column(BigInteger, default=0, nullable=False)
    tokenrefills_personalstats = Column(BigInteger, default=0, nullable=False)
    refills_personalstats = Column(BigInteger, default=0, nullable=False)
    trainsreceived_personalstats = Column(BigInteger, default=0, nullable=False)
    daysbeendonator_personalstats = Column(BigInteger, default=0, nullable=False)
    UpdateDateTime = Column(DateTime)
    age = Column(BigInteger, default=0, nullable=False)
    respectforfaction_personalstats = Column(BigInteger, default=0, nullable=False)
    position_job = Column(String(100), default='0', nullable=False)
    activestreak_personalstats = Column(BigInteger, default=0, nullable=False)
    total_criminalrecord = Column(BigInteger, default=0, nullable=False)
    traveltimes_personalstats = Column(BigInteger, default=0, nullable=False)
    territoryjoins_personalstats = Column(BigInteger, default=0, nullable=False)
    territorytime_personalstats = Column(BigInteger, default=0, nullable=False)
    estimate_active_days = Column(Float, default=0, nullable=False)
    team_competition = Column(String(100))
    useractivity_personalstats = Column(BigInteger, default=0, nullable=False)
    index1 = Index('idx_player_id', player_id)
    index2 = Index('idx_position_job_faction_id', position_job, faction_id_faction, company_id_job, name)
