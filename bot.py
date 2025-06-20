# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os
import datetime
import random
from typing import Optional, List
import uuid
import re

# --- BOT AYARLARI ---
BOT_TOKEN = "MTMzODUxNjc1NzExOTIzODIyNw.GX7smz.J5MlmZI0tkfN3hUcWp9GaDjpzb2J6HifaX1Clo" 
LOG_CHANNEL_ID = 1384591317182713907 
STARTING_BALANCE = 250.0
DAILY_REWARD = 100.0
CRIME_COOLDOWN_HOURS = 6
PRODUCTION_COOLDOWN_HOURS = 8
INVESTMENT_RETURN_RATE = 0.05  # %5 getiri
LOAN_INTEREST_RATE = 0.1  # %10 faiz
MAX_LOAN_AMOUNT = 10000.0
LOAN_COOLDOWN_DAYS = 7
STOCK_EVENT_INTERVAL_HOURS = 12
STOCK_EVENT_CHANCE = 0.3  # %30 şans
MINISTER_SALARY = 5000.0  # Bakan maaşı

# --- DOSYA YOLLARI ---
BASE_DIR = "data"
BUDGET_FILE = os.path.join(BASE_DIR, "budgets.json")
WALLET_FILE = os.path.join(BASE_DIR, "wallets.json")
COMPANY_FILE = os.path.join(BASE_DIR, "companies.json")
ELECTION_FILE = os.path.join(BASE_DIR, "elections.json")
BANK_FILE = os.path.join(BASE_DIR, "bank_accounts.json")
PROFILE_FILE = os.path.join(BASE_DIR, "profiles.json")
DAILY_CLAIMS_FILE = os.path.join(BASE_DIR, "daily_claims.json")
CRIME_COOLDOWNS_FILE = os.path.join(BASE_DIR, "crime_cooldowns.json")
PRODUCTION_COOLDOWNS_FILE = os.path.join(BASE_DIR, "production_cooldowns.json")
CONTRACTS_FILE = os.path.join(BASE_DIR, "contracts.json")
MARKET_FILE = os.path.join(BASE_DIR, "market_listings.json")
STOCK_MARKET_FILE = os.path.join(BASE_DIR, "stock_market.json")
PORTFOLIO_FILE = os.path.join(BASE_DIR, "portfolios.json")
TRANSACTION_LOG_FILE = os.path.join(BASE_DIR, "transactions.json")
LOANS_FILE = os.path.join(BASE_DIR, "loans.json")
INVESTMENTS_FILE = os.path.join(BASE_DIR, "investments.json")
MINISTERS_FILE = os.path.join(BASE_DIR, "ministers.json")
MAIN_BUDGET_KEY = "devlet_kasasi"

# --- ŞİRKET AYARLARI ---
COMPANY_CREATION_COST = 7500.0
COMPANY_TYPES = {
    "madencilik": {"name": "Madencilik Şirketi", "emoji": "⛏️"},
    "ormancılık": {"name": "Ormancılık Şirketi", "emoji": "🌲"},
    "tarım": {"name": "Tarım Çiftliği", "emoji": "🚜"},
    "sanayi": {"name": "Sanayi Tesisi", "emoji": "🏭"},
    "teknoloji": {"name": "Teknoloji Firması", "emoji": "🛰️"},
    "enerji": {"name": "Enerji Şirketi", "emoji": "⚡"}
}
COMPANY_LEVELS = {
    1: {"name": "Küçük İşletme", "cost": 0, "prod_amount": 15},
    2: {"name": "Orta Ölçekli İşletme", "cost": 25000.0, "prod_amount": 35},
    3: {"name": "Büyük İşletme", "cost": 100000.0, "prod_amount": 70},
    4: {"name": "Dev Holding", "cost": 500000.0, "prod_amount": 150}
}
PRODUCTION_RECIPES = {
    "madencilik": {"level": 1, "output": "demir", "amount": 1, "inputs": {}},
    "ormancılık": {"level": 1, "output": "kereste", "amount": 1, "inputs": {}},
    "tarım": {"level": 1, "output": "gıda", "amount": 1, "inputs": {}},
    "sanayi": {"level": 1, "output": "çelik", "amount": 1, "inputs": {"demir": 2}},
    "teknoloji": {"level": 1, "output": "elektronik parça", "amount": 1, "inputs": {"çelik": 1, "demir": 1}},
    "enerji": {"level": 1, "output": "petrol", "amount": 1, "inputs": {}}
}
ALL_PRODUCTS = {
    "demir": {"emoji": "🔩", "base_value": 50}, 
    "gıda": {"emoji": "🍞", "base_value": 30}, 
    "kereste": {"emoji": "🪵", "base_value": 40}, 
    "çelik": {"emoji": "🔗", "base_value": 120}, 
    "elektronik parça": {"emoji": "💡", "base_value": 250},
    "petrol": {"emoji": "🛢️", "base_value": 180}
}
ALL_PRODUCT_CHOICES = [app_commands.Choice(name=f"{name.capitalize()} {data['emoji']}", value=name) for name, data in ALL_PRODUCTS.items()]

# --- BAKANLIK LİSTESİ ---
MINISTRIES = {
    "hazine": {"name": "Hazine Bakanlığı", "emoji": "💰", "budget": 100000.0},
    "savunma": {"name": "Savunma Bakanlığı", "emoji": "🛡️", "budget": 150000.0},
    "adalet": {"name": "Adalet Bakanlığı", "emoji": "⚖️", "budget": 80000.0},
    "içişleri": {"name": "İçişleri Bakanlığı", "emoji": "🏛️", "budget": 120000.0},
    "dışişleri": {"name": "Dışişleri Bakanlığı", "emoji": "🌐", "budget": 90000.0},
    "eğitim": {"name": "Eğitim Bakanlığı", "emoji": "📚", "budget": 130000.0},
    "sağlık": {"name": "Sağlık Bakanlığı", "emoji": "🏥", "budget": 140000.0},
    "tarım": {"name": "Tarım Bakanlığı", "emoji": "🚜", "budget": 110000.0},
    "ticaret": {"name": "Ticaret Bakanlığı", "emoji": "🤝", "budget": 100000.0},
    "ulaştırma_enerji": {"name": "Ulaştırma ve Enerji Bakanlığı", "emoji": "⚡", "budget": 160000.0},
    "gençlik_spor": {"name": "Gençlik ve Spor Bakanlığı", "emoji": "⚽", "budget": 70000.0},
    "iç_güvenlik": {"name": "İç Güvenlik Bakanlığı", "emoji": "👮", "budget": 170000.0}
}
MINISTRY_CHOICES = [app_commands.Choice(name=data["name"], value=key) for key, data in MINISTRIES.items()]
ALL_BUDGET_TARGETS = [app_commands.Choice(name="Devlet Kasası", value=MAIN_BUDGET_KEY)] + MINISTRY_CHOICES

# --- SUÇ TÜRLERİ ---
CRIME_TYPES = {
    "dolandırıcılık": {"name": "Dolandırıcılık", "emoji": "🎭", "min_reward": 100, "max_reward": 500, "min_risk": 0.2, "max_risk": 0.5, "cooldown": 4},
    "soygun": {"name": "Banka Soygunu", "emoji": "🏦", "min_reward": 500, "max_reward": 2000, "min_risk": 0.5, "max_risk": 0.8, "cooldown": 8},
    "hırsızlık": {"name": "Hırsızlık", "emoji": "💎", "min_reward": 50, "max_reward": 300, "min_risk": 0.1, "max_risk": 0.4, "cooldown": 2},
    "veri_hırsızlığı": {"name": "Veri Hırsızlığı", "emoji": "💻", "min_reward": 300, "max_reward": 1000, "min_risk": 0.3, "max_risk": 0.6, "cooldown": 6},
    "kaçakçılık": {"name": "Kaçakçılık", "emoji": "🚢", "min_reward": 800, "max_reward": 3000, "min_risk": 0.6, "max_risk": 0.9, "cooldown": 12}
}
CRIME_TYPE_CHOICES = [app_commands.Choice(name=f"{data['emoji']} {data['name']}", value=crime_type) for crime_type, data in CRIME_TYPES.items()]

# --- BORSA OLAYLARI ---
STOCK_EVENT_TYPES = {
    "boom": {"name": "Borsa Patlaması", "emoji": "🚀", "effect": 0.15},
    "crash": {"name": "Borsa Çöküşü", "emoji": "📉", "effect": -0.15},
    "scandal": {"name": "Skandal", "emoji": "🤫", "effect": -0.25},
    "innovation": {"name": "Yenilik", "emoji": "💡", "effect": 0.25},
    "merger": {"name": "Birleşme", "emoji": "🤝", "effect": 0.20},
    "regulation": {"name": "Regülasyon", "emoji": "📜", "effect": -0.20}
}

# --- YARDIMCI FONKSİYONLAR ---
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_data(file_path, default_data_factory):
    ensure_dir(file_path)
    if not os.path.exists(file_path):
        default_data = default_data_factory()
        with open(file_path, 'w', encoding='utf-8') as f: 
            json.dump(default_data, f, ensure_ascii=False, indent=4)
        return default_data
    try:
        with open(file_path, 'r', encoding='utf-8') as f: 
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, TypeError):
        os.remove(file_path)
        return load_data(file_path, default_data_factory)

def save_data(file_path, data):
    ensure_dir(file_path)
    with open(file_path, 'w', encoding='utf-8') as f: 
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_default_budgets():
    return { 
        MAIN_BUDGET_KEY: 5000000.0, 
        "bakanliklar": {key: data["budget"] for key, data in MINISTRIES.items()}
    }

def get_default_ministers():
    return {key: None for key in MINISTRIES.keys()}

def add_transaction_record(record_text):
    transactions = load_data(TRANSACTION_LOG_FILE, lambda: [])
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%d-%m-%Y %H:%M")
    transactions.insert(0, f"**[{timestamp} UTC]** - {record_text}")
    save_data(TRANSACTION_LOG_FILE, transactions[:100])

async def affect_stock_price(company_name: str, percentage_change: float):
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    stock_id = next((sid for sid, data in stocks.items() if data['name'].lower() == company_name.lower()), None)
    if stock_id:
        new_price = stocks[stock_id]['price'] * (1 + percentage_change)
        stocks[stock_id]['price'] = max(0.01, new_price)
        save_data(STOCK_MARKET_FILE, stocks)
        print(f"Borsa Etkisi: {company_name} hissesi %{percentage_change*100:.2f} değişti.")

def format_money(amount):
    return f"`{amount:,.2f} $`"

def get_ministry_emoji(ministry_key):
    return MINISTRIES[ministry_key]["emoji"] if ministry_key in MINISTRIES else "🏛️"

# --- KALICI BUTON VIEW ---
class PersistentView(discord.ui.View):
    def __init__(self): 
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Kimliğim", style=discord.ButtonStyle.green, custom_id="kimlik_button", emoji="🪪")
    async def show_profile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        user = interaction.user
        profiles = load_data(PROFILE_FILE, lambda: {})
        user_profile = profiles.get(str(user.id))
        if not user_profile:
            await interaction.followup.send("Önce `/kimlik oluştur` komutu ile kimlik kartı oluşturmalısınız.", ephemeral=True)
            return

        wallets = load_data(WALLET_FILE, lambda: {})
        banks = load_data(BANK_FILE, lambda: {})
        companies = load_data(COMPANY_FILE, lambda: {})
        portfolios = load_data(PORTFOLIO_FILE, lambda: {})
        stocks = load_data(STOCK_MARKET_FILE, lambda: {})
        ministers = load_data(MINISTERS_FILE, get_default_ministers)
        
        embed = discord.Embed(title=f"🌟 Yıldızeli Federasyonu Kimlik Kartı", color=user.color if user.color != discord.Color.default() else discord.Color.light_gray())
        embed.set_author(name=f"{user.display_name}", icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="📝 Y.E Numarası", value=f"`{user.id}`", inline=False)
        embed.add_field(name="🎂 Doğum Tarihi", value=user_profile.get("dogum_tarihi", "Belirtilmemiş"), inline=True)
        embed.add_field(name="📖 Biyografi", value=f"```{user_profile.get('biyografi', 'Biyografi yok.')}```", inline=False)

        # Bakanlık bilgisi
        ministry_role = None
        for ministry, minister_id in ministers.items():
            if str(user.id) == minister_id:
                ministry_role = ministry
                break
        
        if ministry_role:
            embed.add_field(name="👑 Bakanlık", value=f"{MINISTRIES[ministry_role]['emoji']} {MINISTRIES[ministry_role]['name']}", inline=False)

        # Finansal bilgiler
        wallet_balance = wallets.get(str(user.id), {}).get("balance", 0)
        bank_balance = banks.get(str(user.id), {}).get("balance", 0)
        assets_text = f"💼 Cüzdan: {format_money(wallet_balance)}\n🏦 Banka: {format_money(bank_balance)}"
        
        # Portföy değeri
        user_portfolio = portfolios.get(str(user.id), {})
        portfolio_value = sum(stock_data['price'] * amount for stock_id, amount in user_portfolio.items() if (stock_data := stocks.get(stock_id)))
        assets_text += f"\n📊 Portföy Değeri: {format_money(portfolio_value)}"
        
        # Şirket bilgisi
        user_company = next((data for data in companies.values() if data['ceo_id'] == str(user.id)), None)
        if user_company:
            level_info = COMPANY_LEVELS.get(user_company['level'], {})
            company_text = f"🏢 Şirket: {user_company['name']}\n⭐ Seviye: {level_info.get('name', 'Bilinmiyor')} (Seviye {user_company['level']})"
            embed.add_field(name="💼 Şirket Bilgisi", value=company_text, inline=False)

        embed.add_field(name="💰 Finansal Durum", value=assets_text, inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)

# --- KOMUT GRUPLARI TANIMLAMALARI ---
bütçe_group = app_commands.Group(name="bütçe", description="Devlet bütçe işlemleri")
cuzdan_group = app_commands.Group(name="cüzdan", description="Kişisel cüzdan işlemleri")
banka_group = app_commands.Group(name="banka", description="Kişisel banka işlemleri")
sirket_group = app_commands.Group(name="sirket", description="Şirket yönetimi ve üretim")
sözleşme_group = app_commands.Group(name="sözleşme", description="Bakanlık sözleşmeleri ve ihaleler")
pazar_group = app_commands.Group(name="pazar", description="Oyuncular arası serbest pazar")
borsa_group = app_commands.Group(name="borsa", description="Hisse senedi alım satımı")
seçim_group = app_commands.Group(name="seçim", description="Seçim ve oylama işlemleri")
suç_group = app_commands.Group(name="suç", description="Yasa dışı faaliyetler")
kimlik_group = app_commands.Group(name="kimlik", description="Kişisel rol yapma kimliğiniz")
admin_group = app_commands.Group(name="admin", description="Yönetici komutları", default_permissions=discord.Permissions(administrator=True))
yatırım_group = app_commands.Group(name="yatırım", description="Şirketlere yatırım yaparak sabit getiri elde edin")
kredi_group = app_commands.Group(name="kredi", description="Devlet kredileri")
bakanlık_group = app_commands.Group(name="bakanlık", description="Bakanlık yönetim komutları")

# --- DÖNGÜLER ve ARKA PLAN GÖREVLERİ ---
@tasks.loop(minutes=1)
async def check_elections_loop():
    await bot.wait_until_ready()
    elections = load_data(ELECTION_FILE, lambda: {})
    now = datetime.datetime.now(datetime.timezone.utc)
    for election_name, data in list(elections.items()):
        if data.get('is_active'):
            end_date = datetime.datetime.fromisoformat(data['end_date'])
            if now >= end_date:
                print(f"'{election_name}' seçimi otomatik olarak bitiriliyor...")
                await finish_election(election_name)

@tasks.loop(hours=4)
async def update_stock_prices():
    await bot.wait_until_ready()
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    if not stocks: return
    
    for stock_id, data in stocks.items():
        change_percent = random.uniform(-0.05, 0.05)
        new_price = data['price'] * (1 + change_percent)
        stocks[stock_id]['price'] = max(0.01, new_price) 
        
    save_data(STOCK_MARKET_FILE, stocks)
    print(f"[{datetime.datetime.now()}] Borsa fiyatları güncellendi.")

@tasks.loop(hours=STOCK_EVENT_INTERVAL_HOURS)
async def trigger_stock_events():
    await bot.wait_until_ready()
    if random.random() > STOCK_EVENT_CHANCE: return
    
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    if not stocks: return
    
    event_type = random.choice(list(STOCK_EVENT_TYPES.keys()))
    event_data = STOCK_EVENT_TYPES[event_type]
    effect = event_data['effect']
    
    stock_id = random.choice(list(stocks.keys()))
    stock_data = stocks[stock_id]
    old_price = stock_data['price']
    new_price = max(0.01, old_price * (1 + effect))
    stock_data['price'] = new_price
    
    save_data(STOCK_MARKET_FILE, stocks)
    
    if LOG_CHANNEL_ID != 0:
        try:
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                embed = discord.Embed(
                    title=f"{event_data['emoji']} Borsa Olayı: {event_data['name']}",
                    description=f"**{stock_data['name']}** hissesi **%{effect*100:.0f}** değişti!\n"
                                f"📉 Eski Fiyat: {format_money(old_price)}\n"
                                f"📈 Yeni Fiyat: {format_money(new_price)}",
                    color=discord.Color.gold() if effect > 0 else discord.Color.red()
                )
                await log_channel.send(embed=embed)
        except Exception as e: 
            print(f"Log kanalına gönderirken hata: {e}")

@tasks.loop(hours=24)
async def process_loan_interest():
    await bot.wait_until_ready()
    loans = load_data(LOANS_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    
    for user_id, user_loans in loans.items():
        for loan_id, loan_data in list(user_loans.items()):
            # Faiz ekle
            loan_data['interest_accumulated'] += loan_data['amount'] * LOAN_INTEREST_RATE
            # Eğer vade dolmuşsa
            due_date = datetime.datetime.fromisoformat(loan_data['due_date'])
            now = datetime.datetime.now(datetime.timezone.utc)
            if now > due_date:
                total_debt = loan_data['amount'] + loan_data['interest_accumulated']
                if wallets.get(user_id, {}).get('balance', 0) >= total_debt:
                    wallets[user_id]['balance'] -= total_debt
                    budgets[MAIN_BUDGET_KEY] += total_debt
                    add_transaction_record(f"**<@{user_id}>** kredisini vadesinde ödeyemedi. {format_money(total_debt)} Devlet Kasası'na aktarıldı.")
                else:
                    budgets[MAIN_BUDGET_KEY] += total_debt
                    add_transaction_record(f"**<@{user_id}>** kredisini ödeyemedi. {format_money(total_debt)} Devlet Kasası'na aktarıldı.")
                del user_loans[loan_id]
    
    save_data(LOANS_FILE, loans)
    save_data(WALLET_FILE, wallets)
    save_data(BUDGET_FILE, budgets)

@tasks.loop(hours=24)
async def pay_minister_salaries():
    await bot.wait_until_ready()
    ministers = load_data(MINISTERS_FILE, get_default_ministers)
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    wallets = load_data(WALLET_FILE, lambda: {})
    
    for ministry, minister_id in ministers.items():
        if minister_id:
            ministry_budget = budgets["bakanliklar"].get(ministry, 0)
            if ministry_budget >= MINISTER_SALARY:
                budgets["bakanliklar"][ministry] -= MINISTER_SALARY
                wallets.setdefault(minister_id, {"balance": 0})["balance"] += MINISTER_SALARY
                add_transaction_record(f"**<@{minister_id}>** {MINISTRIES[ministry]['name']} bakanı olarak {format_money(MINISTER_SALARY)} maaş aldı.")
    
    save_data(BUDGET_FILE, budgets)
    save_data(WALLET_FILE, wallets)

# --- BOT SINIFI ---
class YildizeliBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Komut Gruplarını Bota Ekle
        self.tree.add_command(bütçe_group)
        self.tree.add_command(cuzdan_group)
        self.tree.add_command(banka_group)
        self.tree.add_command(sirket_group)
        self.tree.add_command(sözleşme_group)
        self.tree.add_command(pazar_group)
        self.tree.add_command(borsa_group)
        self.tree.add_command(seçim_group)
        self.tree.add_command(suç_group)
        self.tree.add_command(kimlik_group)
        self.tree.add_command(admin_group)
        self.tree.add_command(yatırım_group)
        self.tree.add_command(kredi_group)
        self.tree.add_command(bakanlık_group)

        # Kalıcı View'i Ekle
        self.add_view(PersistentView())

        # Döngüleri Başlat
        check_elections_loop.start()
        update_stock_prices.start()
        trigger_stock_events.start()
        process_loan_interest.start()
        pay_minister_salaries.start()

        # Komutları Senkronize Et
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user} olarak Discord\'a giriş yapıldı.')
        print(f"Senkronize edilmiş komut sayısı: {len(self.tree.get_commands())}")
        await self.change_presence(activity=discord.Game(name="/yardım"))
        
bot = YildizeliBot()

# --- YARDIMCI LOG FONKSİYONU ---
async def log_action(interaction: discord.Interaction, embed: discord.Embed, transaction_text: str):
    add_transaction_record(transaction_text)
    if LOG_CHANNEL_ID != 0:
        try:
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel: 
                await log_channel.send(embed=embed)
        except Exception as e: 
            print(f"Log kanalına gönderirken hata: {e}")

# --- AUTOCOMPLETE FONKSİYONLARI ---
async def active_election_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    elections = load_data(ELECTION_FILE, lambda: {})
    return [app_commands.Choice(name=name, value=name) for name, data in elections.items() if data.get('is_active', False) and current.lower() in name.lower()][:25]

async def candidate_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    election_name = interaction.namespace.seçim_adı
    if not election_name: return []
    elections = load_data(ELECTION_FILE, lambda: {})
    found_key = next((key for key in elections if key.lower() == election_name.lower()), None)
    if not found_key: return []
    candidates = elections[found_key].get('candidates', {})
    return [app_commands.Choice(name=data['name'], value=user_id) for user_id, data in candidates.items() if current.lower() in data['name'].lower()][:25]
    
async def contract_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    contracts = load_data(CONTRACTS_FILE, lambda: {})
    return [app_commands.Choice(name=f"#{uid[:6]}: {data['product_amount']} {data['product_name']}", value=uid) for uid, data in contracts.items() if current.lower() in data['product_name'] or current in uid][:25]

async def stock_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    return [app_commands.Choice(name=data['name'], value=stock_id) for stock_id, data in stocks.items() if current.lower() in data['name'].lower()][:25]

# --- ANA KOMUTLAR ---
@bot.tree.command(name="yardım", description="Botun komutları hakkında bilgi verir.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="🌟 Yıldızeli Federasyonu Bot Yardım Menüsü", color=discord.Color.blurple())
    embed.add_field(name="🪪 /kimlik", value="Kişisel rol yapma kimliğinizi yönetin.", inline=False)
    embed.add_field(name="💰 /cüzdan", value="Kişisel cüzdanınızı yönetin.", inline=False)
    embed.add_field(name="🏦 /banka", value="Banka hesabınızı yönetin.", inline=False)
    embed.add_field(name="🏢 /sirket", value="Şirketinizi kurun, geliştirin ve üretim yapın.", inline=False)
    embed.add_field(name="📜 /sözleşme", value="Bakanlıkların açtığı ihaleleri görün ve tamamlayın.", inline=False)
    embed.add_field(name="📦 /pazar", value="Oyuncular arası serbest pazarda alım-satım yapın.", inline=False)
    embed.add_field(name="📊 /borsa", value="Şirket hisselerine yatırım yapın.", inline=False)
    embed.add_field(name="🗳️ /seçim", value="Seçimlere katılın ve oy kullanın.", inline=False)
    embed.add_field(name="🎭 /suç", value="Yasa dışı faaliyetlerde bulunun (riskli).", inline=False)
    embed.add_field(name="💼 /yatırım", value="Şirketlere yatırım yapın ve kar elde edin.", inline=False)
    embed.add_field(name="🏦 /kredi", value="Devletten kredi alın ve ödeyin.", inline=False)
    embed.add_field(name="👑 /bakanlık", value="Bakanlık yönetim komutları.", inline=False)
    embed.add_field(name="☀️ /günlük", value="Günlük vatandaşlık gelirinizi alın.", inline=False)
    embed.add_field(name="🎲 /zar", value="Rol yapma için zar atın.", inline=False)
    embed.add_field(name="🏛️ /bütçe", value="Devlet bütçelerini görüntüleyin.", inline=False)
    embed.add_field(name="👮 /admin", value="Yönetici komutları.", inline=False)
    embed.add_field(name="📋 /işlem_geçmişi", value="Son işlemleri gösterin.", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="işlem_geçmişi", description="Son ekonomik işlemleri listeler.")
async def islem_gecmisi(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    transactions = load_data(TRANSACTION_LOG_FILE, lambda: [])
    embed = discord.Embed(title="📜 Son Ekonomik İşlemler", color=discord.Color.light_grey())
    embed.description = "\n".join(transactions) if transactions else "İşlem kaydı bulunamadı."
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="günlük", description="24 saatte bir günlük vatandaşlık gelirinizi alırsınız.")
async def daily_reward(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    now = datetime.datetime.now(datetime.timezone.utc)
    wallets = load_data(WALLET_FILE, lambda: {})
    if user_id not in wallets:
        await interaction.followup.send("Önce `/cüzdan oluştur` komutuyla bir cüzdan oluşturmalısın."); return
    claims = load_data(DAILY_CLAIMS_FILE, lambda: {})
    last_claim_str = claims.get(user_id)
    if last_claim_str:
        last_claim_time = datetime.datetime.fromisoformat(last_claim_str)
        if now < last_claim_time + datetime.timedelta(hours=24):
            time_left = (last_claim_time + datetime.timedelta(hours=24)) - now
            await interaction.followup.send(f"Günlük gelirini zaten aldın. Kalan süre: **{str(time_left).split('.')[0]}**"); return
    wallets[user_id]['balance'] += DAILY_REWARD
    claims[user_id] = now.isoformat()
    save_data(WALLET_FILE, wallets); save_data(DAILY_CLAIMS_FILE, claims)
    embed = discord.Embed(title="☀️ Günlük Gelir Alındı!", description=f"Hesabına **{DAILY_REWARD:,.2f} $** eklendi.", color=discord.Color.yellow())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="zar", description="Rol yapma için zar atar (örn: 1d20, 2d6+3).")
@app_commands.describe(zar_notasyonu="Atılacak zar (örn: '2d8' veya '1d20+4').")
async def roll_dice(interaction: discord.Interaction, zar_notasyonu: str):
    await interaction.response.defer()
    pattern = re.compile(r"(\d+)d(\d+)([\+\-]\d+)?")
    match = pattern.match(zar_notasyonu.lower())
    if not match:
        await interaction.followup.send("Geçersiz zar formatı! Örnek: `1d20`, `3d6`, `1d8+4`"); return
    
    num_dice = int(match.group(1))
    num_sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0

    if num_dice > 100 or num_sides > 1000:
        await interaction.followup.send("Çok fazla zar veya çok büyük bir zar atamazsın!"); return
        
    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    total = sum(rolls) + modifier

    result_str = f"**Sonuç:** {total}\n**Detay:** `{rolls}` + (Mod: {modifier})"
    embed = discord.Embed(title=f"🎲 {interaction.user.display_name}, `{zar_notasyonu}` attı!", description=result_str, color=discord.Color.random())
    await interaction.followup.send(embed=embed)

# --- BÜTÇE GRUBU ---
@bütçe_group.command(name="göster", description="Ülke veya bakanlık bütçelerini listeler.")
@app_commands.describe(bakanlık="Bütçesi görüntülenecek bakanlık (isteğe bağlı).")
@app_commands.choices(bakanlık=MINISTRY_CHOICES)
async def butce_goster(interaction: discord.Interaction, bakanlık: Optional[str] = None):
    await interaction.response.defer()
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    embed = discord.Embed(title="🏛️ Yıldızeli Federasyonu Bütçe Raporu", color=discord.Color.gold())
    devlet_kasasi = budgets.get(MAIN_BUDGET_KEY, 0)
    if bakanlık:
        bütçe_miktari = budgets.get("bakanliklar", {}).get(bakanlık, 0)
        embed.title = f"{MINISTRIES.get(bakanlık, {}).get('name', '')} Bütçesi"
        embed.description = f"### Mevcut Bütçe: {format_money(bütçe_miktari)}"
    else:
        embed.add_field(name="💰 Devlet Kasası", value=f"## {format_money(devlet_kasasi)}", inline=False)
        desc = "".join([f"**{MINISTRIES[key]['emoji']} {MINISTRIES[key]['name']}:** {format_money(budgets.get('bakanliklar', {}).get(key, 0))}\n" for key in MINISTRIES])
        embed.add_field(name="🏛️ Bakanlık Bütçeleri", value=desc, inline=False)
    embed.set_footer(text=f"Devlet Kasası: {format_money(devlet_kasasi)}")
    await interaction.followup.send(embed=embed)

@bütçe_group.command(name="transfer", description="Bütçeler arası para transferi yapar.")
@app_commands.describe(kaynak="Paranın alınacağı bütçe", hedef="Paranın ekleneceği bütçe", miktar="Transfer miktarı")
@app_commands.choices(kaynak=ALL_BUDGET_TARGETS, hedef=ALL_BUDGET_TARGETS)
async def transfer_budget(interaction: discord.Interaction, kaynak: str, hedef: str, miktar: float):
    await interaction.response.defer(ephemeral=True)
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    
    # Kaynak kontrolü
    if kaynak == MAIN_BUDGET_KEY:
        if budgets[MAIN_BUDGET_KEY] < miktar:
            await interaction.followup.send("Devlet kasasında yeterli para yok.")
            return
    else:
        if budgets["bakanliklar"].get(kaynak, 0) < miktar:
            await interaction.followup.send(f"{MINISTRIES[kaynak]['name']} bütçesinde yeterli para yok.")
            return
    
    # Kaynaktan düş
    if kaynak == MAIN_BUDGET_KEY:
        budgets[MAIN_BUDGET_KEY] -= miktar
    else:
        budgets["bakanliklar"][kaynak] -= miktar
    
    # Hedefe ekle
    if hedef == MAIN_BUDGET_KEY:
        budgets[MAIN_BUDGET_KEY] += miktar
    else:
        budgets["bakanliklar"].setdefault(hedef, 0)
        budgets["bakanliklar"][hedef] += miktar
    
    save_data(BUDGET_FILE, budgets)
    
    source_name = "Devlet Kasası" if kaynak == MAIN_BUDGET_KEY else MINISTRIES[kaynak]['name']
    target_name = "Devlet Kasası" if hedef == MAIN_BUDGET_KEY else MINISTRIES[hedef]['name']
    
    embed = discord.Embed(title="✅ Bütçe Transferi Tamamlandı", 
                         description=f"{source_name} bütçesinden {target_name} bütçesine {format_money(miktar)} transfer edildi.",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# --- CÜZDAN GRUBU ---
@cuzdan_group.command(name="oluştur", description="Kendinize ait kişisel bir cüzdan oluşturur.")
async def create_wallet(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    wallets = load_data(WALLET_FILE, lambda: {})
    if user_id in wallets:
        await interaction.followup.send("Zaten bir cüzdanın var!"); return
    wallets[user_id] = {"balance": STARTING_BALANCE}
    save_data(WALLET_FILE, wallets)
    embed = discord.Embed(title="💼 Cüzdan Oluşturuldu!", description=f"{interaction.user.mention}, cüzdanın {format_money(STARTING_BALANCE)} ile oluşturuldu.", color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@cuzdan_group.command(name="bilgi", description="Kendi cüzdan bakiyenizi veya başka birininkini görüntüler.")
@app_commands.describe(kullanıcı="Bakiyesi görüntülenecek kullanıcı (isteğe bağlı).")
async def wallet_info(interaction: discord.Interaction, kullanıcı: Optional[discord.Member] = None):
    target_user = kullanıcı or interaction.user
    await interaction.response.defer(ephemeral=True)
    wallets = load_data(WALLET_FILE, lambda: {})
    if str(target_user.id) not in wallets:
        await interaction.followup.send(f"**{target_user.display_name}** adlı kullanıcının cüzdanı yok."); return
    balance = wallets[str(target_user.id)].get("balance", 0)
    embed = discord.Embed(title=f"💼 {target_user.display_name} Cüzdanı", description=f"### Bakiye: {format_money(balance)}", color=discord.Color.gold())
    await interaction.followup.send(embed=embed)

@cuzdan_group.command(name="transfer", description="Başka bir kullanıcıya para gönderir.")
@app_commands.describe(hedef="Para gönderilecek kullanıcı.", miktar="Gönderilecek miktar.")
async def transfer_money(interaction: discord.Interaction, hedef: discord.Member, miktar: float):
    await interaction.response.defer()
    if miktar <= 0 or hedef.bot or hedef.id == interaction.user.id:
        await interaction.followup.send("Geçersiz miktar veya hedef.", ephemeral=True); return
    wallets = load_data(WALLET_FILE, lambda: {})
    sender_id, receiver_id = str(interaction.user.id), str(hedef.id)
    if sender_id not in wallets or receiver_id not in wallets:
        await interaction.followup.send("İki tarafın da cüzdanı olmalı.", ephemeral=True); return
    if wallets[sender_id].get("balance", 0) < miktar:
        await interaction.followup.send("Yetersiz bakiye.", ephemeral=True); return
    wallets[sender_id]["balance"] -= miktar
    wallets[receiver_id]["balance"] += miktar
    save_data(WALLET_FILE, wallets)
    embed = discord.Embed(title="✅ Para Transferi", color=discord.Color.dark_green())
    embed.add_field(name="Gönderen", value=interaction.user.mention, inline=True)
    embed.add_field(name="Alıcı", value=hedef.mention, inline=True)
    embed.add_field(name="Miktar", value=format_money(miktar), inline=False)
    await log_action(interaction, embed, f"**{interaction.user.mention}**, **{hedef.mention}**'a {format_money(miktar)} transfer etti.")
    await interaction.followup.send(embed=embed)

@cuzdan_group.command(name="sıralama", description="Sunucudaki en zengin 10 vatandaşı listeler.")
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.defer()
    wallets = load_data(WALLET_FILE, lambda: {})
    if not wallets: 
        await interaction.followup.send("Sıralama için cüzdan bulunamadı."); return
    sorted_wallets = sorted(wallets.items(), key=lambda item: item[1]['balance'], reverse=True)
    embed = discord.Embed(title="🏆 Zenginler Listesi", color=discord.Color.yellow())
    desc = ""
    for i, (user_id, data) in enumerate(sorted_wallets[:10]):
        try: 
            user = await bot.fetch_user(int(user_id)); 
            user_name = user.display_name
        except discord.NotFound: 
            user_name = f"Bilinmeyen Kullanıcı"
        emoji = ["🥇", "🥈", "🥉"][i] if i < 3 else f"**{i+1}.**"
        desc += f"{emoji} {user_name} - {format_money(data['balance'])}\n"
    embed.description = desc
    await interaction.followup.send(embed=embed)

# --- BANKA GRUBU ---
@banka_group.command(name="hesap_aç", description="Federasyon bankasında bir hesap açarsınız.")
async def open_bank_account(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    accounts = load_data(BANK_FILE, lambda: {})
    if user_id in accounts:
        await interaction.followup.send("Zaten bir banka hesabınız var."); return
    accounts[user_id] = {'balance': 0.0}
    save_data(BANK_FILE, accounts)
    embed = discord.Embed(title="🏦 Hesap Açıldı!", description="Federasyon bankasında hesabınız başarıyla oluşturuldu.", color=discord.Color.blue())
    await interaction.followup.send(embed=embed)

@banka_group.command(name="bakiye", description="Banka hesabınızdaki bakiyeyi görüntülersiniz.")
async def bank_balance(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    accounts = load_data(BANK_FILE, lambda: {})
    if user_id not in accounts:
        await interaction.followup.send("Önce `/banka hesap_aç` ile bir hesap açmalısınız."); return
    balance = accounts[user_id].get('balance', 0)
    embed = discord.Embed(title=f"🏦 {interaction.user.display_name} Banka Hesabı", description=f"### Bankadaki Bakiye: {format_money(balance)}", color=discord.Color.dark_blue())
    await interaction.followup.send(embed=embed)

@banka_group.command(name="para_yatır", description="Kişisel cüzdanınızdan banka hesabınıza para yatırırsınız.")
@app_commands.describe(miktar="Yatırılacak miktar.")
async def bank_deposit(interaction: discord.Interaction, miktar: float):
    await interaction.response.defer(ephemeral=True)
    if miktar <= 0: await interaction.followup.send("Geçersiz miktar."); return
    user_id = str(interaction.user.id)
    wallets = load_data(WALLET_FILE, lambda: {}); accounts = load_data(BANK_FILE, lambda: {})
    if user_id not in accounts: await interaction.followup.send("Önce bir banka hesabı açmalısınız."); return
    if wallets.get(user_id, {}).get('balance', 0) < miktar: await interaction.followup.send("Cüzdanınızda yeterli para yok."); return
    
    wallets[user_id]['balance'] -= miktar
    accounts[user_id]['balance'] += miktar
    save_data(WALLET_FILE, wallets); save_data(BANK_FILE, accounts)
    embed = discord.Embed(title="✅ Para Yatırıldı", description=f"Banka hesabınıza {format_money(miktar)} yatırdınız.", color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@banka_group.command(name="para_çek", description="Banka hesabınızdan kişisel cüzdanınıza para çekersiniz.")
@app_commands.describe(miktar="Çekilecek miktar.")
async def bank_withdraw(interaction: discord.Interaction, miktar: float):
    await interaction.response.defer(ephemeral=True)
    if miktar <= 0: await interaction.followup.send("Geçersiz miktar."); return
    user_id = str(interaction.user.id)
    wallets = load_data(WALLET_FILE, lambda: {}); accounts = load_data(BANK_FILE, lambda: {})
    if user_id not in accounts: await interaction.followup.send("Önce bir banka hesabı açmalısınız."); return
    if accounts[user_id].get('balance', 0) < miktar: await interaction.followup.send("Banka hesabınızda yeterli para yok."); return
    
    accounts[user_id]['balance'] -= miktar
    wallets.setdefault(user_id, {'balance': 0})['balance'] += miktar
    save_data(WALLET_FILE, wallets); save_data(BANK_FILE, accounts)
    embed = discord.Embed(title="✅ Para Çekildi", description=f"Banka hesabınızdan cüzdanınıza {format_money(miktar)} çektiniz.", color=discord.Color.orange())
    await interaction.followup.send(embed=embed)

# --- KİMLİK GRUBU ---
@kimlik_group.command(name="oluştur", description="Kendinize bir rol yapma kimlik kartı oluşturun.")
@app_commands.describe(biyografi="Kimliğinizde görünecek kısa biyografiniz.", doğum_tarihi="Doğum tarihiniz (örn: 25.05.1990).")
async def create_profile(interaction: discord.Interaction, biyografi: str, doğum_tarihi: str):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    profiles = load_data(PROFILE_FILE, lambda: {})
    if user_id in profiles:
        await interaction.followup.send("Zaten bir kimlik kartınız var. `/kimlik güncelle` ile düzenleyebilirsiniz."); return
        
    profiles[user_id] = {"biyografi": biyografi, "dogum_tarihi": doğum_tarihi}
    save_data(PROFILE_FILE, profiles)
    embed = discord.Embed(title="🪪 Kimlik Oluşturuldu!", description="Federasyon kimlik kartınız başarıyla oluşturuldu.", color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@kimlik_group.command(name="göster", description="Sizin veya başka birinin kimlik kartını gösterir.")
@app_commands.describe(kullanıcı="Kimliği görüntülenecek kullanıcı (isteğe bağlı).")
async def show_profile(interaction: discord.Interaction, kullanıcı: Optional[discord.Member] = None):
    await interaction.response.defer()
    target_user = kullanıcı or interaction.user
    
    profiles = load_data(PROFILE_FILE, lambda: {})
    user_profile = profiles.get(str(target_user.id))
    if not user_profile:
        await interaction.followup.send(f"**{target_user.display_name}** adlı kullanıcının kimlik kartı bulunmuyor.", ephemeral=True); return

    wallets = load_data(WALLET_FILE, lambda: {})
    banks = load_data(BANK_FILE, lambda: {})
    companies = load_data(COMPANY_FILE, lambda: {})
    portfolios = load_data(PORTFOLIO_FILE, lambda: {})
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    ministers = load_data(MINISTERS_FILE, get_default_ministers)

    embed = discord.Embed(color=target_user.color if target_user.color != discord.Color.default() else discord.Color.light_gray())
    embed.set_author(name="🌟 Y.E. FEDERASYONU KİMLİK KARTI", icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
    embed.set_thumbnail(url=target_user.display_avatar.url)
    embed.add_field(name="👤 İsim Soyisim", value=target_user.display_name, inline=True)
    embed.add_field(name="🎂 Doğum Tarihi", value=user_profile.get("dogum_tarihi", "Belirtilmemiş"), inline=True)
    embed.add_field(name="🆔 Y.E. Numarası", value=f"`{target_user.id}`", inline=False)
    embed.add_field(name="📖 Biyografi", value=f"```{user_profile.get('biyografi', 'Biyografi yok.')}```", inline=False)

    # Bakanlık bilgisi
    ministry_role = None
    for ministry, minister_id in ministers.items():
        if str(target_user.id) == minister_id:
            ministry_role = ministry
            break
    
    if ministry_role:
        embed.add_field(name="👑 Bakanlık", value=f"{MINISTRIES[ministry_role]['emoji']} {MINISTRIES[ministry_role]['name']}", inline=False)

    # Finansal bilgiler
    wallet_balance = wallets.get(str(target_user.id), {}).get("balance", 0)
    bank_balance = banks.get(str(target_user.id), {}).get("balance", 0)
    assets_text = f"💼 Cüzdan: {format_money(wallet_balance)}\n🏦 Banka: {format_money(bank_balance)}"
    
    # Portföy değeri
    user_portfolio = portfolios.get(str(target_user.id), {})
    portfolio_value = sum(stock_data['price'] * amount for stock_id, amount in user_portfolio.items() if (stock_data := stocks.get(stock_id)))
    assets_text += f"\n📊 Portföy Değeri: {format_money(portfolio_value)}"
    
    # Şirket bilgisi
    user_company = next((data for data in companies.values() if data['ceo_id'] == str(target_user.id)), None)
    if user_company:
        level_info = COMPANY_LEVELS.get(user_company['level'], {})
        company_text = f"🏢 Şirket: {user_company['name']}\n⭐ Seviye: {level_info.get('name', 'Bilinmiyor')} (Seviye {user_company['level']})"
        embed.add_field(name="💼 Şirket Bilgisi", value=company_text, inline=False)

    embed.add_field(name="💰 Finansal Durum", value=assets_text, inline=False)
    await interaction.followup.send(embed=embed)

@kimlik_group.command(name="güncelle", description="Kimlik kartınızdaki biyografiyi günceller.")
@app_commands.describe(yeni_biyografi="Yeni biyografiniz.")
async def update_profile(interaction: discord.Interaction, yeni_biyografi: str):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    profiles = load_data(PROFILE_FILE, lambda: {})
    if user_id not in profiles:
        await interaction.followup.send("Önce `/kimlik oluştur` ile bir kimlik oluşturmalısınız."); return
    
    profiles[user_id]['biyografi'] = yeni_biyografi
    save_data(PROFILE_FILE, profiles)
    embed = discord.Embed(title="✅ Kimlik Güncellendi", description="Biyografiniz başarıyla güncellendi.", color=discord.Color.blue())
    await interaction.followup.send(embed=embed)

# --- ŞİRKET GRUBU ---
@sirket_group.command(name="oluştur", description="Yeni bir uzmanlık alanında şirket kurun.")
@app_commands.describe(isim="Şirketinizin tam adı.", tür="Şirketinizin uzmanlık alanı.")
@app_commands.choices(tür=[app_commands.Choice(name=data['name'], value=key) for key, data in COMPANY_TYPES.items()])
async def create_company_new(interaction: discord.Interaction, isim: str, tür: str):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    wallets = load_data(WALLET_FILE, lambda: {}); companies = load_data(COMPANY_FILE, lambda: {})
    if wallets.get(user_id, {}).get('balance', 0) < COMPANY_CREATION_COST:
        await interaction.followup.send(f"Şirket kurmak için {format_money(COMPANY_CREATION_COST)} gerekli."); return
    if any(c['ceo_id'] == user_id for c in companies.values()):
        await interaction.followup.send("Zaten bir şirketin CEO'susun!"); return
    if isim.lower() in [k.lower() for k in companies.keys()]:
        await interaction.followup.send("Bu isimde bir şirket zaten var."); return
    wallets[user_id]['balance'] -= COMPANY_CREATION_COST
    companies[isim] = {"name": isim, "ceo_id": user_id, "type": tür, "level": 1, "balance": 0.0, "inventory": {}}
    save_data(WALLET_FILE, wallets); save_data(COMPANY_FILE, companies)
    embed = discord.Embed(title=f"🏢 Şirket Kuruldu!", description=f"Tebrikler, **{isim}** ({COMPANY_TYPES[tür]['name']}) adlı şirketiniz kuruldu!", color=discord.Color.brand_green())
    await log_action(interaction, embed, f"**{interaction.user.mention}**, **{isim}** şirketini kurdu.")
    await interaction.followup.send(embed=embed)
    
@sirket_group.command(name="bilgi", description="Şirketinizin detaylı bilgilerini gösterir.")
@app_commands.describe(isim="Bilgisi görüntülenecek şirketin adı (kendi şirketiniz için boş bırakın).")
async def company_info(interaction: discord.Interaction, isim: Optional[str] = None):
    await interaction.response.defer(ephemeral=True)
    companies = load_data(COMPANY_FILE, lambda: {})
    company_key = None
    if isim:
        company_key = next((key for key in companies if key.lower() == isim.lower()), None)
    else:
        user_id = str(interaction.user.id)
        company_key = next((key for key, c in companies.items() if c['ceo_id'] == user_id), None)
        if not company_key: await interaction.followup.send("Bir şirketiniz yok veya şirket adı belirtmediniz."); return
        
    if not company_key or company_key not in companies: await interaction.followup.send("Bu isimde bir şirket bulunamadı."); return
    company_data = companies[company_key]
    
    ceo = await bot.fetch_user(company_data['ceo_id'])
    company_type_info = COMPANY_TYPES.get(company_data['type'], {"name": "Bilinmeyen", "emoji": "❓"})
    level_info = COMPANY_LEVELS.get(company_data['level'], {"name": "Bilinmeyen"})
    
    embed = discord.Embed(title=f"{company_type_info['emoji']} {company_data['name']}", color=discord.Color.dark_blue())
    embed.add_field(name="👑 CEO", value=ceo.mention, inline=True)
    embed.add_field(name="💰 Kasa", value=format_money(company_data['balance']), inline=True)
    embed.add_field(name="⭐ Seviye", value=f"Seviye {company_data['level']} ({level_info['name']})", inline=True)
    
    inventory = company_data.get('inventory', {})
    desc = "\n".join([f"{ALL_PRODUCTS[item]['emoji']} {item.capitalize()}: `{qty}`" for item, qty in inventory.items()]) if inventory else "Envanter boş."
    embed.add_field(name="📦 Envanter", value=desc, inline=False)
    await interaction.followup.send(embed=embed)
    
@sirket_group.command(name="geliştir", description="Şirketinizi bir üst seviyeye yükseltin.")
async def upgrade_company(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    companies = load_data(COMPANY_FILE, lambda: {})
    company_key = next((key for key, c in companies.items() if c['ceo_id'] == user_id), None)
    if not company_key: await interaction.followup.send("Yönettiğiniz bir şirket bulunamadı."); return

    company_data = companies[company_key]
    current_level = company_data['level']
    next_level = current_level + 1
    
    if next_level not in COMPANY_LEVELS:
        await interaction.followup.send("Şirketiniz zaten son seviyede!"); return
        
    upgrade_cost = COMPANY_LEVELS[next_level]['cost']
    if company_data['balance'] < upgrade_cost:
        await interaction.followup.send(f"Yükseltme için şirket kasasında yeterli para yok. Gerekli: {format_money(upgrade_cost)}"); return
        
    company_data['balance'] -= upgrade_cost
    company_data['level'] = next_level
    save_data(COMPANY_FILE, companies)
    
    await affect_stock_price(company_data['name'], 0.05) # Şirket gelişince hissesi %5 artsın
    
    embed = discord.Embed(title="🚀 Şirket Geliştirildi!", description=f"**{company_data['name']}** şirketi **Seviye {next_level}** ({COMPANY_LEVELS[next_level]['name']}) seviyesine yükseltildi!", color=discord.Color.purple())
    await log_action(interaction, embed, f"**{interaction.user.mention}**, şirketini Seviye {next_level}'e geliştirdi.")
    await interaction.followup.send(embed=embed)

@sirket_group.command(name="üret", description="Şirketinizde üretim yapın (hammadde veya işlenmiş ürün).")
async def produce_items(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    now = datetime.datetime.now(datetime.timezone.utc)
    
    cooldowns = load_data(PRODUCTION_COOLDOWNS_FILE, lambda: {})
    last_prod_str = cooldowns.get(user_id)
    if last_prod_str:
        last_prod_time = datetime.datetime.fromisoformat(last_prod_str)
        if now < last_prod_time + datetime.timedelta(hours=PRODUCTION_COOLDOWN_HOURS):
            time_left = (last_prod_time + datetime.timedelta(hours=PRODUCTION_COOLDOWN_HOURS)) - now
            await interaction.followup.send(f"Çok sık üretim yapamazsın. Kalan süre: **{str(time_left).split('.')[0]}**"); return
    
    companies = load_data(COMPANY_FILE, lambda: {})
    company_key = next((key for key, c in companies.items() if c['ceo_id'] == user_id), None)
    if not company_key: await interaction.followup.send("Yönettiğiniz bir şirket bulunamadı."); return
    
    company_data = companies[company_key]
    company_type = company_data['type']
    level = company_data['level']
    recipe = PRODUCTION_RECIPES.get(company_type)
    if not recipe:
        await interaction.followup.send("Şirket türünüz için bir üretim tarifi bulunamadı."); return
    
    production_amount = COMPANY_LEVELS[level]['prod_amount']
    
    inventory = company_data.setdefault('inventory', {})
    if recipe['inputs']:
        for item, required_amount_per_unit in recipe['inputs'].items():
            total_required = required_amount_per_unit * production_amount
            if inventory.get(item, 0) < total_required:
                await interaction.followup.send(f"Üretim için yeterli hammadde yok. Gerekli: **{total_required}** adet **{item.capitalize()}**"); return
        for item, required_amount_per_unit in recipe['inputs'].items():
            inventory[item] -= required_amount_per_unit * production_amount

    output_item = recipe['output']
    inventory.setdefault(output_item, 0)
    inventory[output_item] += production_amount
    
    embed = discord.Embed(title="🏭 Üretim Tamamlandı!", description=f"Envanterinize **{production_amount}** adet **{output_item.capitalize()}** eklendi.", color=discord.Color.green())

    cooldowns[user_id] = now.isoformat()
    save_data(PRODUCTION_COOLDOWNS_FILE, cooldowns)
    save_data(COMPANY_FILE, companies)
    await log_action(interaction, embed, f"**{interaction.user.mention}**, şirketiyle üretim yaptı.")
    await interaction.followup.send(embed=embed)

# --- PAZAR GRUBU ---
@pazar_group.command(name="liste", description="Pazardaki tüm satış ilanlarını listeler.")
async def market_list(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    market_listings = load_data(MARKET_FILE, lambda: {})
    embed = discord.Embed(title="📦 Oyuncular Arası Pazar", color=discord.Color.dark_orange())
    if not market_listings:
        embed.description = "Pazarda hiç ürün bulunmuyor."
    else:
        desc = ""
        for listing_id, data in market_listings.items():
            try:
                seller = await bot.fetch_user(data['seller_id'])
                seller_name = seller.display_name
            except discord.NotFound:
                seller_name = "Bilinmeyen Satıcı"
            product_emoji = ALL_PRODUCTS.get(data['product'], {}).get("emoji", "")
            desc += f"**ID:** `{listing_id}` - **{data['amount']}** adet {product_emoji} **{data['product'].capitalize()}**\n"
            desc += f"**Fiyat:** {format_money(data['price_per_unit'])} (Toplam: {format_money(data['price_per_unit']*data['amount'])})\n"
            desc += f"**Satıcı:** {seller_name}\n---\n"
        embed.description = desc
    await interaction.followup.send(embed=embed)

@pazar_group.command(name="ilan_ver", description="Envanterinizdeki bir ürünü pazarda satışa çıkarın.")
@app_commands.describe(ürün="Satmak istediğiniz ürün.", adet="Satmak istediğiniz adet.", birim_fiyat="Her bir ürün için istediğiniz fiyat.")
@app_commands.choices(ürün=ALL_PRODUCT_CHOICES)
async def list_on_market(interaction: discord.Interaction, ürün: str, adet: int, birim_fiyat: float):
    await interaction.response.defer(ephemeral=True)
    if adet <= 0 or birim_fiyat <= 0: await interaction.followup.send("Geçersiz adet veya fiyat."); return
    
    user_id = str(interaction.user.id)
    companies = load_data(COMPANY_FILE, lambda: {})
    company_key = next((key for key, c in companies.items() if c['ceo_id'] == user_id), None)
    if not company_key: await interaction.followup.send("Bu komutu kullanmak için bir şirketiniz olmalı."); return
    
    company_data = companies[company_key]
    inventory = company_data.setdefault('inventory', {})
    if inventory.get(ürün, 0) < adet:
        await interaction.followup.send(f"Envanterinizde yeterli **{ürün.capitalize()}** yok."); return
        
    inventory[ürün] -= adet
    if inventory[ürün] == 0: del inventory[ürün]
    
    market_listings = load_data(MARKET_FILE, lambda: {})
    listing_id = str(uuid.uuid4())[:8]
    market_listings[listing_id] = {
        "seller_id": user_id,
        "product": ürün,
        "amount": adet,
        "price_per_unit": birim_fiyat
    }
    
    save_data(COMPANY_FILE, companies)
    save_data(MARKET_FILE, market_listings)
    embed = discord.Embed(title="✅ Pazara İlan Verildi!", description=f"**{adet}** adet **{ürün.capitalize()}** ürününü pazara koydunuz.", color=discord.Color.blue())
    await interaction.followup.send(embed=embed)

@pazar_group.command(name="satın_al", description="Pazardaki bir ilanı şirketinizle satın alın.")
@app_commands.describe(ilan_id="Satın almak istediğiniz ilanın ID'si.", adet="Almak istediğiniz adet.")
async def buy_from_market(interaction: discord.Interaction, ilan_id: str, adet: int):
    await interaction.response.defer(ephemeral=True)
    if adet <= 0: await interaction.followup.send("Geçersiz adet."); return
    
    user_id = str(interaction.user.id)
    market_listings = load_data(MARKET_FILE, lambda: {})
    if ilan_id not in market_listings:
        await interaction.followup.send("Geçersiz ilan ID'si."); return
    
    listing = market_listings[ilan_id]
    if listing['seller_id'] == user_id:
        await interaction.followup.send("Kendi ilanınızı satın alamazsınız."); return
    if listing['amount'] < adet:
        await interaction.followup.send("İlanda yeterli sayıda ürün yok."); return

    companies = load_data(COMPANY_FILE, lambda: {})
    buyer_company_key = next((key for key, c in companies.items() if c['ceo_id'] == user_id), None)
    if not buyer_company_key: await interaction.followup.send("Satın alım yapmak için bir şirketiniz olmalı."); return

    buyer_company = companies[buyer_company_key]
    total_cost = listing['price_per_unit'] * adet
    if buyer_company['balance'] < total_cost:
        await interaction.followup.send(f"Şirketinizin kasasında yeterli para yok. Gerekli: {format_money(total_cost)}"); return
        
    buyer_company['balance'] -= total_cost
    
    seller_company_key = next((key for key, c in companies.items() if c['ceo_id'] == listing['seller_id']), None)
    if seller_company_key:
        companies[seller_company_key]['balance'] += total_cost

    product_name = listing['product']
    buyer_company.setdefault('inventory', {}).setdefault(product_name, 0)
    buyer_company['inventory'][product_name] += adet
    
    listing['amount'] -= adet
    if listing['amount'] == 0:
        del market_listings[ilan_id]
        
    save_data(COMPANY_FILE, companies)
    save_data(MARKET_FILE, market_listings)
    
    embed = discord.Embed(title="✅ Pazardan Alım Yapıldı!", description=f"**{adet}** adet **{product_name.capitalize()}** ürününü satın aldınız.", color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# --- BORSA GRUBU ---
@borsa_group.command(name="hisse_sat", description="Şirketinizi halka arz ederek hisse senedi çıkarın.")
@app_commands.describe(hisse_fiyatı="Hisse başına fiyat.", adet="Satışa çıkarılacak hisse adedi.")
async def ipo_stock(interaction: discord.Interaction, hisse_fiyatı: float, adet: int):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    companies = load_data(COMPANY_FILE, lambda: {})
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    
    company_key = next((key for key, c in companies.items() if c['ceo_id'] == user_id), None)
    if not company_key: 
        await interaction.followup.send("Şirket sahibi değilsiniz."); return
    if company_key in stocks:
        await interaction.followup.send("Şirketiniz zaten halka açık."); return
        
    stock_id = str(uuid.uuid4())
    stocks[stock_id] = {
        "name": company_key,
        "price": hisse_fiyatı,
        "total_shares": adet,
        "available_shares": adet,
        "ceo_id": user_id
    }
    
    save_data(STOCK_MARKET_FILE, stocks)
    embed = discord.Embed(title="🚀 Halka Arz Başarılı!", 
                         description=f"**{company_key}** şirketi hisseleri satışa çıktı!\n"
                                     f"**Fiyat:** {format_money(hisse_fiyatı)}\n"
                                     f"**Adet:** `{adet}`",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@borsa_group.command(name="hisse_al", description="Borsada işlem gören bir şirketin hissesini satın alın.")
@app_commands.describe(hisse_id="Almak istediğiniz hisse ID'si.", adet="Almak istediğiniz adet.")
async def buy_stock(interaction: discord.Interaction, hisse_id: str, adet: int):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    portfolios = load_data(PORTFOLIO_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    
    if hisse_id not in stocks:
        await interaction.followup.send("Geçersiz hisse ID'si."); return
    if adet <= 0: 
        await interaction.followup.send("Geçersiz adet."); return
    
    stock = stocks[hisse_id]
    if stock['available_shares'] < adet:
        await interaction.followup.send("Yeterli hisse bulunmuyor."); return
        
    total_cost = stock['price'] * adet
    if wallets.get(user_id, {}).get('balance', 0) < total_cost:
        await interaction.followup.send(f"Yetersiz bakiye. Gerekli: {format_money(total_cost)}"); return
        
    # Ödeme işlemi
    wallets[user_id]['balance'] -= total_cost
    stock['available_shares'] -= adet
    
    # Portföy güncelleme
    user_portfolio = portfolios.setdefault(user_id, {})
    user_portfolio[hisse_id] = user_portfolio.get(hisse_id, 0) + adet
    
    # CEO'ya ödeme
    ceo_wallet = wallets.setdefault(stock['ceo_id'], {'balance': 0})
    ceo_wallet['balance'] += total_cost
    
    save_data(WALLET_FILE, wallets)
    save_data(STOCK_MARKET_FILE, stocks)
    save_data(PORTFOLIO_FILE, portfolios)
    
    embed = discord.Embed(title="✅ Hisse Satın Alındı!", 
                         description=f"**{stock['name']}** şirketinden **{adet}** adet hisse satın aldınız.\n"
                                     f"**Toplam Tutar:** {format_money(total_cost)}",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@borsa_group.command(name="sat", description="Sahip olduğunuz hisse senetlerini satın.")
@app_commands.describe(hisse_id="Satılacak hisse ID'si", adet="Satılacak adet")
async def sell_stock(interaction: discord.Interaction, hisse_id: str, adet: int):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    portfolios = load_data(PORTFOLIO_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    
    if hisse_id not in stocks:
        await interaction.followup.send("Geçersiz hisse ID'si.")
        return
        
    if adet <= 0:
        await interaction.followup.send("Geçersiz adet.")
        return
        
    user_portfolio = portfolios.get(user_id, {})
    if hisse_id not in user_portfolio or user_portfolio[hisse_id] < adet:
        await interaction.followup.send("Yeterli hisseniz bulunmuyor.")
        return
        
    # Calculate sale amount (with 5% transaction fee)
    stock_price = stocks[hisse_id]["price"]
    total_amount = stock_price * adet
    fee = total_amount * 0.05
    net_amount = total_amount - fee
    
    # Update portfolio
    user_portfolio[hisse_id] -= adet
    if user_portfolio[hisse_id] == 0:
        del user_portfolio[hisse_id]
    
    # Update wallet
    wallets.setdefault(user_id, {"balance": 0})
    wallets[user_id]["balance"] += net_amount
    
    # Update stock market
    stocks[hisse_id]["available_shares"] += adet
    
    # Add fee to government budget
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    budgets[MAIN_BUDGET_KEY] += fee
    
    save_data(PORTFOLIO_FILE, portfolios)
    save_data(WALLET_FILE, wallets)
    save_data(STOCK_MARKET_FILE, stocks)
    save_data(BUDGET_FILE, budgets)
    
    embed = discord.Embed(title="✅ Hisse Satışı", 
                         description=f"**{stocks[hisse_id]['name']}** hissesinden **{adet}** adet sattınız.\n"
                                     f"**Toplam Tutar:** {format_money(total_amount)}\n"
                                     f"**İşlem Ücreti (%%5):** {format_money(fee)}\n"
                                     f"**Net Kazanç:** {format_money(net_amount)}",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# --- SEÇİM GRUBU ---
@seçim_group.command(name="başlat", description="Yeni bir seçim başlatın.")
@app_commands.describe(isim="Seçimin adı", süre_saat="Seçimin süresi (saat)", depozito="Aday olmak için gerekli depozito", bakanlık="İlgili bakanlık (isteğe bağlı)")
@app_commands.choices(bakanlık=MINISTRY_CHOICES)
async def start_election(interaction: discord.Interaction, isim: str, süre_saat: int, depozito: float, bakanlık: Optional[str] = None):
    await interaction.response.defer()
    elections = load_data(ELECTION_FILE, lambda: {})
    if isim in elections:
        await interaction.followup.send("Bu isimde zaten bir seçim var."); return
        
    end_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=süre_saat)
    election_data = {
        "is_active": True,
        "end_date": end_time.isoformat(),
        "deposit_amount": depozito,
        "candidates": {},
        "voters": [],
        "announcement_channel_id": interaction.channel_id
    }
    
    if bakanlık:
        election_data["ministry"] = bakanlık
    
    elections[isim] = election_data
    save_data(ELECTION_FILE, elections)
    
    ministry_text = f" ({MINISTRIES[bakanlık]['name']} için)" if bakanlık else ""
    embed = discord.Embed(title="🗳️ Yeni Seçim Başladı!", 
                         description=f"**{isim}**{ministry_text} seçimi başladı!\n"
                                     f"**Bitiş:** <t:{int(end_time.timestamp())}:R>\n"
                                     f"**Adaylık Depozitosu:** {format_money(depozito)}",
                         color=discord.Color.blue())
    await interaction.followup.send(embed=embed)

@seçim_group.command(name="aday_ol", description="Aktif bir seçimde aday olun.")
@app_commands.describe(seçim_ismi="Aday olmak istediğiniz seçimin adı")
async def become_candidate(interaction: discord.Interaction, seçim_ismi: str):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    elections = load_data(ELECTION_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    
    if seçim_ismi not in elections:
        await interaction.followup.send("Böyle bir seçim bulunamadı."); return
    if not elections[seçim_ismi]['is_active']:
        await interaction.followup.send("Bu seçim aktif değil."); return
        
    deposit = elections[seçim_ismi]['deposit_amount']
    if wallets.get(user_id, {}).get('balance', 0) < deposit:
        await interaction.followup.send(f"Yetersiz bakiye. Gerekli depozito: {format_money(deposit)}"); return
        
    # Depozitoyu al
    wallets[user_id]['balance'] -= deposit
    elections[seçim_ismi]['candidates'][user_id] = {
        "name": interaction.user.display_name,
        "votes": 0
    }
    
    save_data(ELECTION_FILE, elections)
    save_data(WALLET_FILE, wallets)
    
    embed = discord.Embed(title="🎉 Adaylık Başvurusu", 
                         description=f"**{seçim_ismi}** seçimine aday oldunuz!\n"
                                     f"{format_money(deposit)} depozitonuz alındı.",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@seçim_group.command(name="oy_ver", description="Aktif bir seçimde oy kullanın.")
@app_commands.describe(seçim_ismi="Oy vereceğiniz seçimin adı", aday="Oy vereceğiniz adayın adı")
async def vote_in_election(interaction: discord.Interaction, seçim_ismi: str, aday: str):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    elections = load_data(ELECTION_FILE, lambda: {})
    
    if seçim_ismi not in elections:
        await interaction.followup.send("Böyle bir seçim bulunamadı."); return
    if not elections[seçim_ismi]['is_active']:
        await interaction.followup.send("Bu seçim aktif değil."); return
        
    # Kullanıcı zaten oy kullanmış mı?
    if user_id in elections[seçim_ismi]['voters']:
        await interaction.followup.send("Bu seçimde zaten oy kullandınız."); return
        
    # Adayı bul
    candidate = None
    for candidate_id, data in elections[seçim_ismi]['candidates'].items():
        if data['name'].lower() == aday.lower():
            candidate = candidate_id
            break
    
    if not candidate:
        await interaction.followup.send("Böyle bir aday bulunamadı."); return
        
    # Oy ver
    elections[seçim_ismi]['candidates'][candidate]['votes'] += 1
    elections[seçim_ismi]['voters'].append(user_id)
    save_data(ELECTION_FILE, elections)
    
    embed = discord.Embed(title="✅ Oy Kullanıldı", 
                         description=f"**{seçim_ismi}** seçiminde **{aday}** adayına oy verdiniz.",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

# --- SUÇ GRUBU ---
@suç_group.command(name="işle", description="Yasa dışı bir faaliyet gerçekleştirin.")
@app_commands.describe(suç_türü="İşlemek istediğiniz suç türü")
@app_commands.choices(suç_türü=CRIME_TYPE_CHOICES)
async def commit_crime(interaction: discord.Interaction, suç_türü: str):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    now = datetime.datetime.now(datetime.timezone.utc)
    cooldowns = load_data(CRIME_COOLDOWNS_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    
    crime_data = CRIME_TYPES[suç_türü]
    cooldown_hours = crime_data['cooldown']
    
    last_crime_str = cooldowns.get(user_id, {}).get(suç_türü)
    if last_crime_str:
        last_crime_time = datetime.datetime.fromisoformat(last_crime_str)
        if now < last_crime_time + datetime.timedelta(hours=cooldown_hours):
            time_left = (last_crime_time + datetime.timedelta(hours=cooldown_hours)) - now
            await interaction.followup.send(f"Bu suçu çok sık işleyemezsin. Kalan süre: **{str(time_left).split('.')[0]}**"); return
    
    # Rastgele sonuç (Başarılı/Başarısız)
    risk = random.uniform(crime_data['min_risk'], crime_data['max_risk'])
    success = random.random() > risk
    
    if success:
        reward = random.uniform(crime_data['min_reward'], crime_data['max_reward'])
        wallets.setdefault(user_id, {'balance': 0})['balance'] += reward
        result_text = f"✅ Başarılı! {format_money(reward)} kazandınız."
        color = discord.Color.green()
    else:
        fine = random.uniform(crime_data['min_reward'], crime_data['max_reward']) / 2
        if wallets.get(user_id, {}).get('balance', 0) < fine:
            fine = wallets[user_id]['balance']  # Tüm parasını al
        if fine > 0:
            wallets[user_id]['balance'] -= fine
            result_text = f"❌ Yakalandınız! {format_money(fine)} ceza ödediniz."
        else:
            result_text = "❌ Yakalandınız ama ödeyecek paranız yok!"
        color = discord.Color.red()
    
    # Cooldown'u güncelle
    if user_id not in cooldowns:
        cooldowns[user_id] = {}
    cooldowns[user_id][suç_türü] = now.isoformat()
    
    save_data(CRIME_COOLDOWNS_FILE, cooldowns)
    save_data(WALLET_FILE, wallets)
    
    embed = discord.Embed(title=f"{crime_data['emoji']} {crime_data['name']}", description=result_text, color=color)
    await interaction.followup.send(embed=embed)

# --- YATIRIM GRUBU ---
@yatırım_group.command(name="yap", description="Bir şirkete yatırım yaparak sabit getiri elde edin.")
@app_commands.describe(şirket="Yatırım yapılacak şirket", miktar="Yatırım miktarı")
async def make_investment(interaction: discord.Interaction, şirket: str, miktar: float):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    wallets = load_data(WALLET_FILE, lambda: {})
    companies = load_data(COMPANY_FILE, lambda: {})
    investments = load_data(INVESTMENTS_FILE, lambda: {})
    
    if miktar <= 0:
        await interaction.followup.send("Geçersiz miktar."); return
    if wallets.get(user_id, {}).get('balance', 0) < miktar:
        await interaction.followup.send("Yetersiz bakiye."); return
    if şirket not in companies:
        await interaction.followup.send("Böyle bir şirket bulunamadı."); return
        
    # Yatırım yap
    wallets[user_id]['balance'] -= miktar
    companies[şirket]['balance'] += miktar
    
    investment_id = str(uuid.uuid4())
    investments.setdefault(user_id, {})[investment_id] = {
        "company": şirket,
        "amount": miktar,
        "return_amount": miktar * (1 + INVESTMENT_RETURN_RATE),
        "claim_date": (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)).isoformat()
    }
    
    save_data(WALLET_FILE, wallets)
    save_data(COMPANY_FILE, companies)
    save_data(INVESTMENTS_FILE, investments)
    
    embed = discord.Embed(
        title="✅ Yatırım Yapıldı!",
        description=f"**{şirket}** şirketine {format_money(miktar)} yatırım yaptınız.\n"
                    f"**24 saat sonra** {format_money(miktar * INVESTMENT_RETURN_RATE)} kar alabileceksiniz.",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

@yatırım_group.command(name="getirisi_al", description="Vadesi dolan yatırımlarınızın getirisini alın.")
async def claim_investment(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    investments = load_data(INVESTMENTS_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    
    user_investments = investments.get(user_id, {})
    if not user_investments:
        await interaction.followup.send("Hiç yatırımınız yok."); return
        
    now = datetime.datetime.now(datetime.timezone.utc)
    total_return = 0
    to_remove = []
    
    for investment_id, data in user_investments.items():
        claim_date = datetime.datetime.fromisoformat(data['claim_date'])
        if now >= claim_date:
            return_amount = data['return_amount'] - data['amount']  # Sadece kar
            wallets.setdefault(user_id, {'balance': 0})['balance'] += return_amount
            total_return += return_amount
            to_remove.append(investment_id)
    
    for investment_id in to_remove:
        del user_investments[investment_id]
    
    if not to_remove:
        await interaction.followup.send("Henüz alınabilecek getiriniz yok."); return
    
    save_data(INVESTMENTS_FILE, investments)
    save_data(WALLET_FILE, wallets)
    
    embed = discord.Embed(
        title="💰 Yatırım Getirisi Alındı!",
        description=f"Toplam {format_money(total_return)} getiri aldınız.",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

# --- KREDİ GRUBU ---
@kredi_group.command(name="al", description="Devletten kredi alın.")
@app_commands.describe(miktar="Almak istediğiniz kredi miktarı", vade_gün="Vade süresi (gün)")
async def take_loan(interaction: discord.Interaction, miktar: float, vade_gün: int):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    loans = load_data(LOANS_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    
    if miktar <= 0 or vade_gün <= 0:
        await interaction.followup.send("Geçersiz miktar veya vade."); return
    if miktar > MAX_LOAN_AMOUNT:
        await interaction.followup.send(f"En fazla {format_money(MAX_LOAN_AMOUNT)} kredi alabilirsiniz."); return
    if budgets[MAIN_BUDGET_KEY] < miktar:
        await interaction.followup.send("Devlet kasasında yeterli para yok."); return
        
    # Kullanıcının aktif kredilerini kontrol et
    user_loans = loans.get(user_id, {})
    if len(user_loans) >= 3:
        await interaction.followup.send("En fazla 3 kredi alabilirsiniz."); return
        
    # Kredi ver
    loan_id = str(uuid.uuid4())
    due_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=vade_gün)
    
    user_loans[loan_id] = {
        "amount": miktar,
        "due_date": due_date.isoformat(),
        "interest_accumulated": 0.0
    }
    
    loans[user_id] = user_loans
    wallets.setdefault(user_id, {'balance': 0})['balance'] += miktar
    budgets[MAIN_BUDGET_KEY] -= miktar
    
    save_data(LOANS_FILE, loans)
    save_data(WALLET_FILE, wallets)
    save_data(BUDGET_FILE, budgets)
    
    embed = discord.Embed(
        title="✅ Kredi Alındı!",
        description=f"{format_money(miktar)} kredi aldınız.\n"
                    f"**Vade:** {vade_gün} gün sonra (<t:{int(due_date.timestamp())}:R>)\n"
                    f"**Faiz Oranı:** %{LOAN_INTEREST_RATE*100:.0f} (günlük)",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

@kredi_group.command(name="öde", description="Kredinizi erken ödeyin.")
@app_commands.describe(kredi_id="Ödemek istediğiniz kredinin ID'si")
async def pay_loan(interaction: discord.Interaction, kredi_id: str):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    loans = load_data(LOANS_FILE, lambda: {})
    wallets = load_data(WALLET_FILE, lambda: {})
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    
    user_loans = loans.get(user_id, {})
    if kredi_id not in user_loans:
        await interaction.followup.send("Geçersiz kredi ID'si."); return
        
    loan_data = user_loans[kredi_id]
    total_amount = loan_data['amount'] + loan_data['interest_accumulated']
    
    if wallets.get(user_id, {}).get('balance', 0) < total_amount:
        await interaction.followup.send(f"Yetersiz bakiye. Gerekli: {format_money(total_amount)}"); return
        
    wallets[user_id]['balance'] -= total_amount
    budgets[MAIN_BUDGET_KEY] += total_amount
    del user_loans[kredi_id]
    
    save_data(LOANS_FILE, loans)
    save_data(WALLET_FILE, wallets)
    save_data(BUDGET_FILE, budgets)
    
    embed = discord.Embed(
        title="✅ Kredi Ödendi!",
        description=f"{format_money(total_amount)} ödeyerek kredinizi kapattınız.",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

@kredi_group.command(name="listele", description="Aktif kredilerinizi listeler.")
async def list_loans(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    loans = load_data(LOANS_FILE, lambda: {})
    user_loans = loans.get(user_id, {})
    
    if not user_loans:
        await interaction.followup.send("Aktif krediniz bulunmamaktadır."); return
        
    embed = discord.Embed(title="📋 Aktif Kredileriniz", color=discord.Color.blue())
    for loan_id, data in user_loans.items():
        due_date = datetime.datetime.fromisoformat(data['due_date'])
        total_amount = data['amount'] + data['interest_accumulated']
        embed.add_field(
            name=f"Kredi ID: `{loan_id}`",
            value=f"**Ana Para:** {format_money(data['amount'])}\n"
                  f"**Birikmiş Faiz:** {format_money(data['interest_accumulated'])}\n"
                  f"**Toplam Borç:** {format_money(total_amount)}\n"
                  f"**Vade Tarihi:** <t:{int(due_date.timestamp())}:R>",
            inline=False
        )
    
    await interaction.followup.send(embed=embed)

# --- BAKANLIK GRUBU ---
@bakanlık_group.command(name="göster", description="Bakanlık bilgilerini gösterir.")
@app_commands.describe(bakanlık="Gösterilecek bakanlık")
@app_commands.choices(bakanlık=MINISTRY_CHOICES)
async def show_ministry(interaction: discord.Interaction, bakanlık: str):
    await interaction.response.defer()
    ministers = load_data(MINISTERS_FILE, get_default_ministers)
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    
    minister_id = ministers.get(bakanlık)
    minister_user = await bot.fetch_user(int(minister_id)) if minister_id else None
    
    embed = discord.Embed(title=f"{MINISTRIES[bakanlık]['emoji']} {MINISTRIES[bakanlık]['name']}", color=discord.Color.dark_purple())
    embed.add_field(name="👑 Bakan", value=minister_user.mention if minister_user else "Atanmamış", inline=True)
    embed.add_field(name="💰 Bütçe", value=format_money(budgets["bakanliklar"].get(bakanlık, 0)), inline=True)
    
    await interaction.followup.send(embed=embed)

@bakanlık_group.command(name="maaş_al", description="Bakanlık maaşınızı alın.")
async def claim_salary(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id = str(interaction.user.id)
    ministers = load_data(MINISTERS_FILE, get_default_ministers)
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    wallets = load_data(WALLET_FILE, lambda: {})
    
    # Kullanıcının bakan olduğu bakanlığı bul
    ministry = None
    for m, minister_id in ministers.items():
        if minister_id == user_id:
            ministry = m
            break
    
    if not ministry:
        await interaction.followup.send("Bakan değilsiniz."); return
        
    # Bakanlık bütçesini kontrol et
    ministry_budget = budgets["bakanliklar"].get(ministry, 0)
    if ministry_budget < MINISTER_SALARY:
        await interaction.followup.send(f"{MINISTRIES[ministry]['name']} bütçesinde yeterli para yok."); return
        
    # Maaşı öde
    budgets["bakanliklar"][ministry] -= MINISTER_SALARY
    wallets.setdefault(user_id, {"balance": 0})["balance"] += MINISTER_SALARY
    
    save_data(BUDGET_FILE, budgets)
    save_data(WALLET_FILE, wallets)
    
    embed = discord.Embed(
        title="💰 Maaş Alındı!",
        description=f"{MINISTRIES[ministry]['name']} bakanı olarak {format_money(MINISTER_SALARY)} maaş aldınız.",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

# --- ADMIN GRUBU ---
@admin_group.command(name="kimlik_düzenle", description="Bir kullanıcının kimlik bilgilerini düzenler.")
@app_commands.describe(kullanıcı="Düzenlenecek kullanıcı", yeni_biyografi="Yeni biyografi", yeni_dogum_tarihi="Yeni doğum tarihi")
async def edit_profile(interaction: discord.Interaction, kullanıcı: discord.User, yeni_biyografi: str, yeni_dogum_tarihi: str):
    await interaction.response.defer(ephemeral=True)
    profiles = load_data(PROFILE_FILE, lambda: {})
    user_id = str(kullanıcı.id)
    
    if user_id not in profiles:
        await interaction.followup.send("Bu kullanıcının kimlik kartı bulunmamaktadır.")
        return
        
    profiles[user_id]["biyografi"] = yeni_biyografi
    profiles[user_id]["dogum_tarihi"] = yeni_dogum_tarihi
    save_data(PROFILE_FILE, profiles)
    
    embed = discord.Embed(title="✅ Kimlik Güncellendi", 
                         description=f"{kullanıcı.mention} kullanıcısının kimlik bilgileri güncellendi.",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@admin_group.command(name="para_ver", description="Bir kullanıcıya para verir.")
@app_commands.describe(kullanıcı="Para verilecek kullanıcı", miktar="Verilecek miktar", kaynak="Paranın alınacağı kaynak")
@app_commands.choices(kaynak=ALL_BUDGET_TARGETS)
async def give_money(interaction: discord.Interaction, kullanıcı: discord.User, miktar: float, kaynak: str):
    await interaction.response.defer(ephemeral=True)
    wallets = load_data(WALLET_FILE, lambda: {})
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    
    if kaynak == MAIN_BUDGET_KEY:
        if budgets[MAIN_BUDGET_KEY] < miktar:
            await interaction.followup.send("Devlet kasasında yeterli para yok.")
            return
        budgets[MAIN_BUDGET_KEY] -= miktar
    else:
        if budgets["bakanliklar"].get(kaynak, 0) < miktar:
            await interaction.followup.send(f"{MINISTRIES[kaynak]['name']} bütçesinde yeterli para yok.")
            return
        budgets["bakanliklar"][kaynak] -= miktar
    
    wallets.setdefault(str(kullanıcı.id), {"balance": 0})
    wallets[str(kullanıcı.id)]["balance"] += miktar
    
    save_data(WALLET_FILE, wallets)
    save_data(BUDGET_FILE, budgets)
    
    source_name = MINISTRIES.get(kaynak, "Devlet Kasası")["name"] if kaynak != MAIN_BUDGET_KEY else "Devlet Kasası"
    embed = discord.Embed(title="✅ Para Transferi", 
                         description=f"{kullanıcı.mention} kullanıcısına {source_name}'ndan {format_money(miktar)} verildi.",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@admin_group.command(name="para_al", description="Bir kullanıcıdan para alır.")
@app_commands.describe(kullanıcı="Parası alınacak kullanıcı", miktar="Alınacak miktar", hedef="Paranın ekleneceği hedef")
@app_commands.choices(hedef=ALL_BUDGET_TARGETS)
async def take_money(interaction: discord.Interaction, kullanıcı: discord.User, miktar: float, hedef: str):
    await interaction.response.defer(ephemeral=True)
    wallets = load_data(WALLET_FILE, lambda: {})
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    user_id = str(kullanıcı.id)
    
    if user_id not in wallets or wallets[user_id]["balance"] < miktar:
        await interaction.followup.send("Kullanıcının yeterli parası yok.")
        return
        
    wallets[user_id]["balance"] -= miktar
    
    if hedef == MAIN_BUDGET_KEY:
        budgets[MAIN_BUDGET_KEY] += miktar
    else:
        budgets["bakanliklar"].setdefault(hedef, 0)
        budgets["bakanliklar"][hedef] += miktar
    
    save_data(WALLET_FILE, wallets)
    save_data(BUDGET_FILE, budgets)
    
    target_name = MINISTRIES.get(hedef, "Devlet Kasası")["name"] if hedef != MAIN_BUDGET_KEY else "Devlet Kasası"
    embed = discord.Embed(title="✅ Para Alındı", 
                         description=f"{kullanıcı.mention} kullanıcısından {format_money(miktar)} alındı ve {target_name}'na eklendi.",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@admin_group.command(name="bütçe_ayarla", description="Bir bütçenin miktarını belirler.")
@app_commands.describe(hedef="Hedef bütçe", miktar="Yeni miktar")
@app_commands.choices(hedef=ALL_BUDGET_TARGETS)
async def set_budget(interaction: discord.Interaction, hedef: str, miktar: float):
    await interaction.response.defer(ephemeral=True)
    budgets = load_data(BUDGET_FILE, get_default_budgets)
    
    if hedef == MAIN_BUDGET_KEY:
        budgets[MAIN_BUDGET_KEY] = miktar
    else:
        budgets["bakanliklar"][hedef] = miktar
    
    save_data(BUDGET_FILE, budgets)
    
    target_name = MINISTRIES.get(hedef, "Devlet Kasası")["name"] if hedef != MAIN_BUDGET_KEY else "Devlet Kasası"
    embed = discord.Embed(title="✅ Bütçe Ayarla", 
                         description=f"{target_name} bütçesi {format_money(miktar)} olarak ayarlandı.",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@admin_group.command(name="sözleşme_oluştur", description="Yeni bir devlet sözleşmesi oluşturur.")
@app_commands.describe(ürün="Sözleşme ürünü", adet="Ürün adedi", bakanlık="Sorumlu bakanlık")
@app_commands.choices(ürün=ALL_PRODUCT_CHOICES, bakanlık=MINISTRY_CHOICES)
async def create_contract(interaction: discord.Interaction, ürün: str, adet: int, bakanlık: str):
    await interaction.response.defer()
    contracts = load_data(CONTRACTS_FILE, lambda: {})
    contract_id = str(uuid.uuid4())[:8]
    
    contracts[contract_id] = {
        "product": ürün,
        "amount": adet,
        "ministry": bakanlık,
        "status": "active",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    save_data(CONTRACTS_FILE, contracts)
    
    embed = discord.Embed(title="📜 Yeni Devlet Sözleşmesi", 
                         description=f"**{MINISTRIES[bakanlık]['name']}** için **{adet}** adet **{ürün.capitalize()}** alım sözleşmesi oluşturuldu!",
                         color=discord.Color.blue())
    await interaction.followup.send(embed=embed)

@admin_group.command(name="halka_arz", description="Bir şirketi zorla halka açar.")
@app_commands.describe(şirket="Halka arz edilecek şirket", hisse_fiyatı="Hisse başına fiyat", adet="Satışa çıkarılacak hisse adedi")
async def force_ipo(interaction: discord.Interaction, şirket: str, hisse_fiyatı: float, adet: int):
    await interaction.response.defer(ephemeral=True)
    companies = load_data(COMPANY_FILE, lambda: {})
    stocks = load_data(STOCK_MARKET_FILE, lambda: {})
    
    if şirket not in companies:
        await interaction.followup.send("Böyle bir şirket bulunamadı.")
        return
        
    if şirket in [s["name"] for s in stocks.values()]:
        await interaction.followup.send("Bu şirket zaten halka açık.")
        return
        
    stock_id = str(uuid.uuid4())
    stocks[stock_id] = {
        "name": şirket,
        "price": hisse_fiyatı,
        "total_shares": adet,
        "available_shares": adet,
        "ceo_id": companies[şirket]["ceo_id"]
    }
    
    save_data(STOCK_MARKET_FILE, stocks)
    
    embed = discord.Embed(title="🚀 Zorunlu Halka Arz", 
                         description=f"**{şirket}** şirketi halka arz edildi!\n"
                                     f"**Fiyat:** {format_money(hisse_fiyatı)}\n"
                                     f"**Adet:** `{adet}`",
                         color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@admin_group.command(name="seçim_başlat", description="Yeni bir seçim başlatır.")
@app_commands.describe(isim="Seçimin adı", süre_saat="Seçim süresi (saat)", depozito="Adaylık depozitosu", bakanlık="İlgili bakanlık (isteğe bağlı)")
@app_commands.choices(bakanlık=MINISTRY_CHOICES)
async def admin_start_election(interaction: discord.Interaction, isim: str, süre_saat: int, depozito: float, bakanlık: Optional[str] = None):
    await interaction.response.defer()
    elections = load_data(ELECTION_FILE, lambda: {})
    
    if isim in elections:
        await interaction.followup.send("Bu isimde zaten bir seçim var.")
        return
        
    end_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=süre_saat)
    election_data = {
        "is_active": True,
        "end_date": end_time.isoformat(),
        "deposit_amount": depozito,
        "candidates": {},
        "voters": [],
        "announcement_channel_id": interaction.channel_id
    }
    
    if bakanlık:
        election_data["ministry"] = bakanlık
    
    elections[isim] = election_data
    save_data(ELECTION_FILE, elections)
    
    ministry_text = f" ({MINISTRIES[bakanlık]['name']} için)" if bakanlık else ""
    embed = discord.Embed(title="🗳️ Yeni Seçim Başladı!", 
                         description=f"**{isim}**{ministry_text} seçimi başladı!\n"
                                     f"**Bitiş:** <t:{int(end_time.timestamp())}:R>\n"
                                     f"**Adaylık Depozitosu:** {format_money(depozito)}",
                         color=discord.Color.blue())
    await interaction.followup.send(embed=embed)

@admin_group.command(name="seçim_bitir", description="Aktif bir seçimi erken bitirir.")
@app_commands.describe(seçim_ismi="Bitirilecek seçimin adı")
async def finish_election_admin(interaction: discord.Interaction, seçim_ismi: str):
    await interaction.response.defer()
    result = await finish_election(seçim_ismi)
    await interaction.followup.send(result)

# --- DİĞER GEREKLİ FONKSİYONLAR ---
async def finish_election(election_name: str) -> str:
    elections = load_data(ELECTION_FILE, lambda: {})
    election_data = elections.get(election_name)
    if not election_data or not election_data.get('is_active'): 
        return "Böyle aktif bir seçim bulunamadı."
    
    election_data['is_active'] = False
    save_data(ELECTION_FILE, elections)
    
    candidates = election_data.get('candidates', {})
    channel_id = election_data['announcement_channel_id']
    if not candidates:
        try:
            channel = await bot.fetch_channel(channel_id)
            await channel.send(f"**{election_name}** seçimi, aday olmadığı için sonuçsuz sona erdi.")
        except Exception as e: print(f"Duyuru kanalına gönderilemedi: {e}")
        return f"**{election_name}** seçimi aday olmadığı için bitirildi."
    sorted_candidates = sorted(candidates.items(), key=lambda item: item[1]['votes'], reverse=True)
    max_votes = sorted_candidates[0][1]['votes']
    winners = {uid: data for uid, data in sorted_candidates if data['votes'] == max_votes and max_votes > 0}
    wallets, budgets, deposit = load_data(WALLET_FILE, lambda: {}), load_data(BUDGET_FILE, get_default_budgets), election_data.get('deposit_amount', 0)
    for user_id, data in candidates.items():
        if user_id in winners:
            wallets.setdefault(user_id, {'balance': 0})['balance'] += deposit
            add_transaction_record(f"**<@{user_id}>**, **{election_name}** seçimini kazandığı için {format_money(deposit)} depozito iadesi aldı.")
        else:
            budgets[MAIN_BUDGET_KEY] += deposit
            add_transaction_record(f"**<@{user_id}>**, **{election_name}** seçimini kaybettiği için {format_money(deposit)} depozitosu Devlet Kasası'na aktarıldı.")
    save_data(WALLET_FILE, wallets); save_data(BUDGET_FILE, budgets)
    
    newspaper_header = "🗞️ **YILDIZELİ HABER AJANSI - SON DAKİKA** 🗞️"
    total_votes = sum(c['votes'] for c in candidates.values())
    
    if not winners:
         announcement_message = (f"{newspaper_header}\n\n@everyone\n\n**{election_name}** seçimleri, geçerli bir kazanan çıkmadığı için sonuçsuz kalmıştır.")
    else:
        winner_mentions = [f"**<@{uid}>**" for uid in winners]
        announcement_message = (
            f"{newspaper_header}\n\n@everyone\n\n"
            f"**{election_name}** seçimleri sona erdi! Toplam **{total_votes}** oy kullanıldı ve seçimin galibi, **{max_votes}** oy alarak "
            f"{', '.join(winner_mentions)} oldu! Tebrikler!\n\n--- **SEÇİM SONUÇLARI** ---\n"
        )
        results_text = "".join([f"{'🏆' if uid in winners else '🔻'} **{data['name']}**: `{data['votes']}` oy\n" for uid, data in sorted_candidates])
        announcement_message += results_text
    
    try:
        channel = await bot.fetch_channel(channel_id); await channel.send(announcement_message, allowed_mentions=discord.AllowedMentions(everyone=True))
    except Exception as e:
        print(f"Duyuru kanalına gönderilemedi: {e}"); return "Seçim bitti, sonuçlar duyurulamadı."
    return f"**{election_name}** seçimi başarıyla bitirildi ve sonuçlar duyuruldu."

# --- HATA YÖNETİMİ ---
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    message = "🤔 Bir şeyler ters gitti! Komut işlenirken bir hata oluştu."
    if isinstance(error, app_commands.errors.MissingPermissions):
        message = "⛔ Bu komutu kullanmak için yetkin yok!"
    else: 
        print(f"Komut Hatası: {error}")
    try:
        if interaction.response.is_done(): 
            await interaction.followup.send(message, ephemeral=True)
        else: 
            await interaction.response.send_message(message, ephemeral=True)
    except discord.errors.InteractionResponded:
        await interaction.followup.send(message, ephemeral=True)
        
# --- BOTU ÇALIŞTIR ---
if __name__ == "__main__":
    if BOT_TOKEN == "MTMzODUxNjc1NzExOTIzODIyNw.GLTxkf.gclIdWqPDCElNIVGSXR8nzfIIcqVw67qHNjeUw":
        print("HATA: Lütfen kodun 13. satırına Discord Bot Token'ınızı girin!")
    else:
        bot.run(BOT_TOKEN)
