import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
import json
from typing import Optional, Dict
import config
from utils import emojis
from database.db_manager import DatabaseManager

# --- CONSTANTS & CONFIGURATION ---

RARITIES = {
    "Common":    {"color": 0x95A5A6, "chance": 50, "mul": 1.0, "emoji": "⚪"},
    "Uncommon":  {"color": 0x2ECC71, "chance": 30, "mul": 1.5, "emoji": "🟢"},
    "Rare":      {"color": 0x3498DB, "chance": 12, "mul": 3.0, "emoji": "🔵"},
    "Epic":      {"color": 0x9B59B6, "chance": 6,  "mul": 8.0, "emoji": "🟣"},
    "Legendary": {"color": 0xF1C40F, "chance": 1.8, "mul": 20.0, "emoji": "🟡"},
    "Mythical":  {"color": 0xE74C3C, "chance": 0.2, "mul": 100.0, "emoji": "🔴"}
}

BIOMES = {
    "Lake": {
        "name": "Hồ Nước",
        "desc": "Nơi bắt đầu yên bình.",
        "req_xp": 0,
        "req_money": 0,
        "emoji": "🏞️",
        "fish": [
            {"name": "Cá Chép", "base_value": 5, "min_size": 10, "max_size": 30},
            {"name": "Cá Rô", "base_value": 8, "min_size": 5, "max_size": 15},
            {"name": "Cá Trê", "base_value": 12, "min_size": 20, "max_size": 50},
            {"name": "Rùa Hồ", "base_value": 50, "min_size": 20, "max_size": 40}, # Rare+
        ]
    },
    "River": {
        "name": "Dòng Sông",
        "desc": "Dòng nước chảy xiết, cá khỏe hơn.",
        "req_xp": 500,
        "req_money": 5000,
        "emoji": "uWQ",
        "fish": [
            {"name": "Cá Hồi", "base_value": 20, "min_size": 30, "max_size": 80},
            {"name": "Cá Lăng", "base_value": 35, "min_size": 40, "max_size": 100},
            {"name": "Ba Ba", "base_value": 80, "min_size": 20, "max_size": 50},
            {"name": "Cá Sấu Con", "base_value": 200, "min_size": 50, "max_size": 150},
        ]
    },
    "Ocean": {
        "name": "Đại Dương",
        "desc": "Biển cả mênh mông với những loài cá lớn.",
        "req_xp": 2000,
        "req_money": 20000,
        "emoji": "🌊",
        "fish": [
            {"name": "Cá Ngừ", "base_value": 100, "min_size": 50, "max_size": 200},
            {"name": "Cá Thu", "base_value": 80, "min_size": 40, "max_size": 120},
            {"name": "Mực Ống", "base_value": 150, "min_size": 20, "max_size": 60},
            {"name": "Cá Mập", "base_value": 500, "min_size": 200, "max_size": 500},
        ]
    },
    "Deep Sea": {
        "name": "Biển Sâu",
        "desc": "Vùng nước tối tăm áp lực cao.",
        "req_xp": 10000,
        "req_money": 50000,
        "emoji": "🦑",
        "fish": [
            {"name": "Cá Lồng Đèn", "base_value": 300, "min_size": 10, "max_size": 40},
            {"name": "Cá Mặt Trăng", "base_value": 800, "min_size": 100, "max_size": 300},
            {"name": "Mực Khổng Lồ", "base_value": 1500, "min_size": 300, "max_size": 1000},
        ]
    },
    "Volcano": {
        "name": "Núi Lửa",
        "desc": "Vùng nước sôi sục, chỉ những loài cá huyền thoại.",
        "req_xp": 50000,
        "req_money": 200000,
        "emoji": "🌋",
        "fish": [
            {"name": "Cá Dung Nham", "base_value": 2000, "min_size": 50, "max_size": 150},
            {"name": "Rồng Lửa", "base_value": 5000, "min_size": 200, "max_size": 800},
            {"name": "Phượng Hoàng Nước", "base_value": 10000, "min_size": 100, "max_size": 300},
        ]
    }
}

RODS = {
    "Plastic Rod":    {"price": 0,       "power": 0,   "luck": 0},
    "Improved Rod":   {"price": 2000,    "power": 5,   "luck": 2},
    "Glass Rod":      {"price": 10000,   "power": 10,  "luck": 5},
    "Carbon Rod":     {"price": 50000,   "power": 20,  "luck": 10},
    "Master Rod":     {"price": 200000,  "power": 35,  "luck": 15},
    "Legendary Rod":  {"price": 1000000, "power": 50,  "luck": 25},
    "Poseidon Rod":   {"price": 5000000, "power": 80,  "luck": 40},
}
ROD_LIST = list(RODS.keys())

BAITS = {
    "Worms":           {"price": 50,    "power": 0,  "luck": 0, "desc": "Mồi câu cơ bản."},
    "Crickets":        {"price": 150,   "power": 2,  "luck": 1, "desc": "Thu hút cá nhỏ."},
    "Leeches":         {"price": 500,   "power": 5,  "luck": 2, "desc": "Bám dính tốt, khó hụt."},
    "Minnows":         {"price": 1500,  "power": 8,  "luck": 5, "desc": "Dụ cá săn mồi."},
    "Squid":           {"price": 3000,  "power": 10, "luck": 8, "desc": "Mồi yêu thích của cá biển."},
    "Cut Bait":        {"price": 5000,  "power": 15, "luck": 10, "desc": "Mùi tanh thu hút cá lớn."},
    "Spinner":         {"price": 10000, "power": 20, "luck": 12, "desc": "Lấp lánh, dụ cá hiếm."},
    "Magic Lure":      {"price": 25000, "power": 30, "luck": 20, "desc": "Có ma thuật, tăng mạnh tỉ lệ."},
    "Golden Grub":     {"price": 50000, "power": 40, "luck": 35, "desc": "Mạ vàng, cá Legendary thích nó."},
    "Rainbow Essence": {"price": 100000,"power": 50, "luck": 50, "desc": "Tinh hoa cầu vồng, mồi tối thượng."}
}

class FishingView(discord.ui.View):
    def __init__(self, cog, user_id, current_biome, last_catch=None):
        super().__init__(timeout=60)
        self.cog = cog
        self.user_id = user_id
        self.current_biome = current_biome
        self.last_catch = last_catch # {name, value} of the fish just caught
        self.message = None

    @discord.ui.button(label="Câu Tiếp", style=discord.ButtonStyle.success, emoji="🎣")
    async def fish_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
        
        # Reset timeout
        self.timeout = 60
        await interaction.response.defer()
        await self.cog.process_fishing(interaction, self.current_biome, view=self)

    @discord.ui.button(label="Bán Nhanh", style=discord.ButtonStyle.secondary, emoji="💰")
    async def sell_fast(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return
            
        if not self.last_catch:
            await interaction.response.send_message("❌ Không có cá để bán hoặc đã bán rồi!", ephemeral=True)
            return

        fish_name = self.last_catch['name']
        fish_value = self.last_catch['value']
        
        # Remove fish from inventory and add money
        # Since we just added it, we decrement count and value
        data = await self.cog.db.get_fishing_data(self.user_id)
        inv = data.get("inventory", {})
        fish_inv = inv.get("fish", {})
        
        if fish_name in fish_inv and fish_inv[fish_name]["count"] > 0:
            fish_inv[fish_name]["count"] -= 1
            fish_inv[fish_name]["total_value"] -= fish_value
            if fish_inv[fish_name]["count"] <= 0:
                del fish_inv[fish_name]
                
            await self.cog.db.update_fishing_data(self.user_id, inventory=inv)
            await self.cog.db.add_points(self.user_id, interaction.guild_id, fish_value)
            
            button.disabled = True
            button.label = "Đã Bán"
            self.last_catch = None # Prevent double sell
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(f"✅ Đã bán **{fish_name}** với giá **{fish_value:,}** Coinz!", ephemeral=True)
        else:
             await interaction.response.send_message("❌ Cá này không còn trong túi đồ (có thể đã bán?)", ephemeral=True)

class CauCaCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db: DatabaseManager):
        self.bot = bot
        self.db = db

    @app_commands.command(name="kenh-cau-ca", description="Set kênh hiện tại làm kênh câu cá")
    @app_commands.checks.has_permissions(administrator=True)
    async def kenh_cau_ca(self, interaction: discord.Interaction):
        """Đặt kênh hiện tại làm kênh chuyên câu cá"""
        await self.db.set_channel_config(interaction.channel_id, interaction.guild_id, "fishing")
        await interaction.response.send_message(
            f"✅ Đã đặt kênh {interaction.channel.mention} làm kênh **Câu Cá**! 🎣\nNgười chơi có thể bắt đầu bằng lệnh `/fish`.",
            ephemeral=False
        )

    async def get_stats_multiplier(self, user_id):
        """Calculate total Power and Luck from Rod + Bait"""
        data = await self.db.get_fishing_data(user_id)
        stats = data.get("stats", {})
        
        # Rod Stats
        rod_name = data.get("rod_type", "Plastic Rod")
        rod = RODS.get(rod_name, RODS["Plastic Rod"])
        
        # Bait Stats
        bait_name = stats.get("current_bait")
        bait = BAITS.get(bait_name, {"power": 0, "luck": 0})
        
        total_power = rod["power"] + bait["power"]
        total_luck = rod["luck"] + bait["luck"]
        
        return total_power, total_luck, data, bait_name

    def calculate_catch(self, biome_name, power, luck):
        """Logic chính xác định kết quả câu cá"""
        biome = BIOMES[biome_name]
        
        # 1. Miss Chance (Base 30%, reduced by Power)
        miss_chance = max(5, 30 - power * 0.5)
        if random.uniform(0, 100) < miss_chance:
            return None # Missed
            
        # 2. Determine Rarity
        # Luck increases chance to roll higher rarities
        roll = random.uniform(0, 100) - (luck * 0.5) 
        
        rarity_name = "Common"
        # Check from rarest to common
        if roll <= RARITIES["Mythical"]["chance"]: rarity_name = "Mythical"
        elif roll <= RARITIES["Legendary"]["chance"]: rarity_name = "Legendary"
        elif roll <= RARITIES["Epic"]["chance"]: rarity_name = "Epic"
        elif roll <= RARITIES["Rare"]["chance"]: rarity_name = "Rare"
        elif roll <= RARITIES["Uncommon"]["chance"]: rarity_name = "Uncommon"
        
        # 3. Determine Fish Specie
        # Filter fish by rarity? Or just pick random from biome and apply rarity modifier?
        # User requested: "cho mỗi loại hiếm 1 màu khác nhau".
        # Let's simplify: Fish species are generic to biome, Rarity is an applied attribute.
        fish_specie = random.choice(biome["fish"])
        
        # 4. Determine Size
        # Size = Base * Random(0.8 -> 1.5) + Power Bonus
        # Power helps catch bigger fish
        size_mult = random.uniform(0.8, 1.2) + (power * 0.01)
        # Rarity greatly boosts size
        rarity_size_bonus = {"Common": 1, "Uncommon": 1.2, "Rare": 1.5, "Epic": 2, "Legendary": 3, "Mythical": 5}
        
        base_size = random.uniform(fish_specie["min_size"], fish_specie["max_size"])
        final_size = base_size * size_mult * rarity_size_bonus[rarity_name]
        
        # 5. Determine Value
        # Value = Base * Size * Rarity_Mult
        rarity_val_mult = RARITIES[rarity_name]["mul"]
        value = int(fish_specie["base_value"] * (final_size / 20) * rarity_val_mult)
        if value < 1: value = 1
        
        return {
            "name": fish_specie["name"],
            "rarity": rarity_name,
            "size": round(final_size, 2),
            "value": value,
            "emoji": RARITIES[rarity_name]["emoji"],
            "color": RARITIES[rarity_name]["color"]
        }

    async def process_fishing(self, interaction: discord.Interaction, biome_name, view=None):
        # Validate Channel (Optional)
        game_type = await self.db.get_channel_config(interaction.channel_id)
        if game_type != "fishing":
            await interaction.followup.send("❌ Kênh này không phải hồ câu! (Admin hãy dùng `/kenh-cau-ca`)", ephemeral=True)
            return

        user_id = interaction.user.id
        power, luck, data, bait_name = await self.get_stats_multiplier(user_id)
        inventory = data.get("inventory", {})
        stats = data.get("stats", {})
        
        # Check Bait Consumption
        bait_consumed = False
        if bait_name:
            baits_inv = inventory.get("baits", {})
            if baits_inv.get(bait_name, 0) > 0:
                baits_inv[bait_name] -= 1
                bait_consumed = True
                if baits_inv[bait_name] <= 0:
                    stats["current_bait"] = None
                    del baits_inv[bait_name]
            else:
                stats["current_bait"] = None # Ran out
                
        # Treasure Chance (2% + Luck)
        treasure_chance = 2 + (luck * 0.1)
        if random.uniform(0, 100) < treasure_chance:
            # TREASURE EVENT
            bonus_coinz = random.randint(1000, 5000) * (1 + luck*0.05)
            await self.db.add_points(user_id, interaction.guild_id, int(bonus_coinz))
            
            embed = discord.Embed(title="🎁 BẠN CÂU ĐƯỢC KHO BÁU!", color=discord.Color.gold())
            embed.description = f"Bên trong rương là **{int(bonus_coinz):,}** Coinz {emojis.ANIMATED_EMOJI_COINZ}!"
            embed.set_footer(text="May mắn quá!")
        else:
            # FISHING EVENT
            result = self.calculate_catch(biome_name, power, luck)
            
            if not result:
                embed = discord.Embed(description=f"🎣 ... Bạn ngồi đợi mãi nhưng không có gì cắn câu. {emojis.SAD}", color=discord.Color.light_grey())
                if bait_consumed:
                    embed.set_footer(text=f"Đã mất 1 {bait_name}...")
            else:
                # Add to inventory
                fish_inv = inventory.get("fish", {})
                f_name = result["name"]
                
                # We store simplified inventory: Name -> {count, total_value}
                # To distinguish rarities in storage would be complex for this simple JSON structure without bloating it.
                # User asked for sell price depends on size/rarity.
                # SOLUTION: Calculate value NOW and store it in the "bag".
                
                if f_name not in fish_inv:
                    fish_inv[f_name] = {"count": 0, "total_value": 0}
                
                fish_inv[f_name]["count"] += 1
                fish_inv[f_name]["total_value"] += result["value"]
                
                # Calc XP
                xp_gain = int(result["value"] / 5)
                stats["xp"] = stats.get("xp", 0) + xp_gain
                
                embed = discord.Embed(title=f"🎣 CÂU ĐƯỢC CÁ!", color=result["color"])
                embed.description = (
                    f"**{result['emoji']} {result['name']}**\n"
                    f"Độ hiếm: **{result['rarity']}**\n"
                    f"Kích thước: **{result['size']}cm**\n"
                    f"Giá trị: **{result['value']:,}** Coinz {emojis.ANIMATED_EMOJI_COINZ}\n"
                    f"Exp: +{xp_gain}"
                )
                if result['rarity'] in ["Legendary", "Mythical"]:
                    embed.set_image(url="https://media.discordapp.net/attachments/123456789/legendary_fish.gif") # Placeholder
        
        # Save DB
        await self.db.update_fishing_data(user_id, inventory=inventory, stats=stats)
        
        # Response
        if view:
            # Update view state for new catch if applicable
            if result:
                 view.last_catch = {'name': result['name'], 'value': result['value']}
                 # Re-enable sell button if it was disabled
                 for child in view.children:
                     if isinstance(child, discord.ui.Button) and child.custom_id == "sell_fast": 
                         # Note: custom_id isn't explicitly set above, so we check label or method
                         pass
                 
                 # Re-instantiate view to reset buttons state cleanly (easiest way)
                 new_view = FishingView(self, user_id, biome_name, last_catch={'name': result['name'], 'value': result['value']})
                 new_view.message = view.message
                 view = new_view # Swap to new view

            if view.message:
                await view.message.edit(embed=embed, view=view)
            else:
                msg = await interaction.followup.send(embed=embed, view=view)
                view.message = msg
        else:
            # First time call
            last_catch_data = None
            if result:
                last_catch_data = {'name': result['name'], 'value': result['value']}
                
            view = FishingView(self, user_id, biome_name, last_catch=last_catch_data)
            msg = await interaction.followup.send(embed=embed, view=view)
            view.message = msg

    @app_commands.command(name="fish", description="Bắt đầu câu cá!")
    async def fish(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        data = await self.db.get_fishing_data(interaction.user.id)
        current_biome = data.get("stats", {}).get("current_biome", "Lake")
        
        # Trigger fishing
        await self.process_fishing(interaction, current_biome)

    @app_commands.command(name="khu-vuc", description="Xem và di chuyển đến các khu vực câu cá")
    async def biomes_cmd(self, interaction: discord.Interaction):
        data = await self.db.get_fishing_data(interaction.user.id)
        stats = data.get("stats", {})
        current = stats.get("current_biome", "Lake")
        unlocked = stats.get("unlocked_biomes", ["Lake"])
        xp = stats.get("xp", 0)
        
        embed = discord.Embed(title="🗺️ BẢN ĐỒ CÂU CÁ", color=discord.Color.teal())
        embed.description = f"Hiện tại đang ở: **{BIOMES[current]['emoji']} {BIOMES[current]['name']}**\nKinh nghiệm (XP): **{xp:,}**"
        
        view = discord.ui.View()
        
        async def unlock_or_travel(interaction: discord.Interaction, biome_key: str):
            # Refresh data
            d = await self.db.get_fishing_data(interaction.user.id)
            s = d.get("stats", {})
            u = s.get("unlocked_biomes", ["Lake"])
            
            if biome_key in u:
                s["current_biome"] = biome_key
                await self.db.update_fishing_data(interaction.user.id, stats=s)
                await interaction.response.send_message(f"✈️ Đã chuyển đến **{BIOMES[biome_key]['name']}**!", ephemeral=True)
            else:
                # Try unlock
                cost = BIOMES[biome_key]["req_money"]
                req_xp = BIOMES[biome_key]["req_xp"]
                
                u_bal = await self.db.get_player_points(interaction.user.id, interaction.guild_id)
                curr_xp = s.get("xp", 0)
                
                if curr_xp < req_xp:
                    await interaction.response.send_message(f"❌ Bạn chưa đủ {req_xp:,} XP để mở khóa!", ephemeral=True)
                    return
                if u_bal < cost:
                    await interaction.response.send_message(f"❌ Bạn không đủ {cost:,} Coinz để mở khóa!", ephemeral=True)
                    return
                
                await self.db.add_points(interaction.user.id, interaction.guild_id, -cost)
                u.append(biome_key)
                s["unlocked_biomes"] = u
                s["current_biome"] = biome_key
                await self.db.update_fishing_data(interaction.user.id, stats=s)
                await interaction.response.send_message(f"🎉 Đã mở khóa và chuyển đến **{BIOMES[biome_key]['name']}**!", ephemeral=True)

        for key, info in BIOMES.items():
            is_unlocked = key in unlocked
            status = "✅ Đang ở" if key == current else ("🔓 Đã mở" if is_unlocked else "🔒 Khóa")
            
            field_val = f"{info['desc']}\n"
            if not is_unlocked:
                field_val += f"Yêu cầu: {info['req_xp']} XP | {info['req_money']:,} Coinz"
            
            embed.add_field(name=f"{info['emoji']} {info['name']} ({status})", value=field_val, inline=False)
            
            # Button logic requires dynamic callback binding or custom class, simulating simplified:
            # Ideally use a Select Menu for biomes if many
            pass 

        # Using Select Menu for Biomes
        select = discord.ui.Select(placeholder="Chọn khu vực để đi...")
        
        for key, info in BIOMES.items():
            label = info['name']
            desc_s = "Đã mở khóa" if key in unlocked else f"Cần {info['req_xp']} XP, {info['req_money']} coinz"
            emoji = info['emoji']
            select.add_option(label=label, value=key, description=desc_s, emoji=emoji)
        
        async def select_callback(inter):
            val = select.values[0]
            await unlock_or_travel(inter, val)
        
        select.callback = select_callback
        view.add_item(select)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="moi-cau", description="Cửa hàng mồi câu")
    async def bait_shop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🪱 CỬA HÀNG MỒI CÂU", description="Mua mồi để tăng tỉ lệ câu!", color=discord.Color.dark_green())
        
        select = discord.ui.Select(placeholder="Mua mồi câu...")
        
        for name, info in BAITS.items():
            embed.add_field(
                name=f"{name} ({info['price']:,} Coinz)",
                value=f"💪 Power: +{info['power']} | 🍀 Luck: +{info['luck']}\n*{info['desc']}*",
                inline=False
            )
            select.add_option(label=f"{name} - {info['price']:,} Coinz", value=name, description=f"Mua 10x {name}")

        async def buy_bait(inter):
            b_name = select.values[0]
            cost = BAITS[b_name]["price"] * 10
            
            points = await self.db.get_player_points(inter.user.id, inter.guild_id)
            if points < cost:
                await inter.response.send_message("❌ Không đủ tiền!", ephemeral=True)
                return

            await self.db.add_points(inter.user.id, inter.guild_id, -cost)
            
            data = await self.db.get_fishing_data(inter.user.id)
            inv = data.get("inventory", {})
            if "baits" not in inv: inv["baits"] = {}
            
            inv["baits"][b_name] = inv["baits"].get(b_name, 0) + 10
            
            # Auto equip if none
            stats = data.get("stats", {})
            if not stats.get("current_bait"):
                 stats["current_bait"] = b_name
            
            await self.db.update_fishing_data(inter.user.id, inventory=inv, stats=stats)
            await inter.response.send_message(f"✅ Đã mua 10x **{b_name}**! (Đang trang bị: {stats['current_bait']})", ephemeral=True)

        select.callback = buy_bait
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="can-cau", description="Cửa hàng & Trang bị cần câu")
    async def rod_shop(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        data = await self.db.get_fishing_data(user_id)
        current_rod = data.get("rod_type", "Plastic Rod")
        
        embed = discord.Embed(title="🎣 CỬA HÀNG CẦN CÂU", color=discord.Color.blue())
        embed.description = f"Cần câu hiện tại: **{current_rod}**"

        # Find next rod
        try:
            curr_idx = ROD_LIST.index(current_rod)
        except:
            current_rod = "Plastic Rod"
            curr_idx = 0
            
        view = discord.ui.View()
        
        if curr_idx < len(ROD_LIST) - 1:
            next_rod = ROD_LIST[curr_idx + 1]
            info = RODS[next_rod]
            
            embed.add_field(
                name="Nâng cấp tiếp theo", 
                value=f"**{next_rod}**\n💰 Giá: {info['price']:,} Coinz\n💪 Power: {info['power']}\n🍀 Luck: {info['luck']}",
                inline=False
            )
            
            btn = discord.ui.Button(label=f"Mua {next_rod}", style=discord.ButtonStyle.primary, emoji="🆙")
            
            async def buy_rod(inter):
                points = await self.db.get_player_points(inter.user.id, inter.guild_id)
                if points < info['price']:
                    await inter.response.send_message("❌ Không đủ tiền!", ephemeral=True)
                    return
                
                await self.db.add_points(inter.user.id, inter.guild_id, -info['price'])
                await self.db.update_fishing_data(inter.user.id, rod_type=next_rod)
                await inter.response.send_message(f"✅ Đã nâng cấp lên **{next_rod}** thành công!", ephemeral=True)
                
            btn.callback = buy_rod
            view.add_item(btn)
        else:
            embed.description += "\n✨ Bạn đã sở hữu cần câu tối thượng!"

        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="inventory", description="Xem túi cá")
    async def inventory(self, interaction: discord.Interaction):
        data = await self.db.get_fishing_data(interaction.user.id)
        inv = data.get("inventory", {})
        fish_inv = inv.get("fish", {})
        baits_inv = inv.get("baits", {})
        
        embed = discord.Embed(title=f"🎒 TÚI ĐỒ CỦA {interaction.user.display_name.upper()}", color=discord.Color.green())
        
        # Fish List
        f_list = []
        total_val = 0
        for name, info in fish_inv.items():
            count = info.get("count", 0)
            val = info.get("total_value", 0)
            if count > 0:
                f_list.append(f"• {name}: x{count} (Tổng: {val:,} Coinz)")
                total_val += val
        
        if f_list:
            embed.add_field(name=f"🐟 Cá ({total_val:,} Coinz)", value="\n".join(f_list[:15]) + ("\n..." if len(f_list)>15 else ""), inline=False)
        else:
            embed.add_field(name="🐟 Cá", value="Trống", inline=False)

        # Bait List
        b_list = []
        for name, count in baits_inv.items():
            if count > 0:
                b_list.append(f"• {name}: x{count}")
        
        if b_list:
            embed.add_field(name="🪱 Mồi Câu", value="\n".join(b_list), inline=False)
        else:
            embed.add_field(name="🪱 Mồi Câu", value="Trống", inline=False)
            
        # Stats
        stats = data.get("stats", {})
        embed.set_footer(text=f"Level: {stats.get('level', 1)} | XP: {stats.get('xp', 0)} | Mồi đang dùng: {stats.get('current_bait', 'Không')}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sell", description="Bán tất cả cá")
    async def sell(self, interaction: discord.Interaction):
        data = await self.db.get_fishing_data(interaction.user.id)
        inv = data.get("inventory", {})
        fish_inv = inv.get("fish", {})
        
        if not fish_inv:
             await interaction.response.send_message("🎒 Không có cá để bán!", ephemeral=True)
             return

        total_payout = 0
        for name, info in fish_inv.items():
            total_payout += info.get("total_value", 0)
            
        if total_payout == 0:
             await interaction.response.send_message("🎒 Không có cá có giá trị để bán!", ephemeral=True)
             return

        # Clear fish
        inv["fish"] = {}
        await self.db.update_fishing_data(interaction.user.id, inventory=inv)
        await self.db.add_points(interaction.user.id, interaction.guild_id, total_payout)
        
        await interaction.response.send_message(f"💰 Đã bán sạch cá và nhận được **{total_payout:,}** Coinz {emojis.ANIMATED_EMOJI_COINZ}!")

async def setup(bot: commands.Bot):
    db = DatabaseManager(config.DATABASE_PATH)
    await bot.add_cog(CauCaCog(bot, db))
