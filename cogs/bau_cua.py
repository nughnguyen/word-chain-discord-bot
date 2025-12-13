import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import config
from utils import emojis
from database.db_manager import DatabaseManager

class BetModal(discord.ui.Modal):
    def __init__(self, side_name, side_emoji, max_bet, current_balance, callback_func):
        super().__init__(title=f"Đặt Cược: {side_name}")
        self.max_bet = max_bet
        self.current_balance = current_balance
        self.callback_func = callback_func
        self.side_name = side_name
        self.side_emoji = side_emoji

        self.amount = discord.ui.TextInput(
            label=f"Số tiền cược (Max {max_bet:,})",
            placeholder="Nhập số tiền...",
            min_length=1,
            max_length=10,
            required=True
        )
        self.add_item(self.amount)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = int(self.amount.value.replace(',', '').replace('.', ''))
            if amount <= 0:
                await interaction.response.send_message("❌ Số tiền cược phải lớn hơn 0!", ephemeral=True)
                return
            
            if amount > self.max_bet:
                await interaction.response.send_message(f"❌ Cược tối đa là {self.max_bet:,} coinz!", ephemeral=True)
                return

            # Check logic, but don't deduct yet.
            # However, we need to track "potential spend" to prevent over-betting across multiple clicks
            # callback_func handles the validation of "locked" funds.
            await self.callback_func(interaction, amount, self.side_name, self.side_emoji)

        except ValueError:
            await interaction.response.send_message("❌ Vui lòng nhập số hợp lệ!", ephemeral=True)

class BauCuaView(discord.ui.View):
    def __init__(self, bot, db, host_id, timeout=120):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.db = db
        self.host_id = host_id
        self.bets = {} # {user_id: {side: amount}}
        self.user_total_bet = {} # {user_id: total_amount}
        self.locked_balance = {} # {user_id: locked_amount}
        self.message = None
        self.stop_event = asyncio.Event()
        
        # Define sides with names and emojis
        self.sides = [
            {"id": "side_1", "name": "Alien", "emoji": emojis.SIDE_1},
            {"id": "side_2", "name": "Star", "emoji": emojis.SIDE_2},
            {"id": "side_3", "name": "Rocket", "emoji": emojis.SIDE_3},
            {"id": "side_4", "name": "Planet", "emoji": emojis.SIDE_4},
            {"id": "side_5", "name": "Galaxy", "emoji": emojis.SIDE_5},
            {"id": "side_6", "name": "Comet", "emoji": emojis.SIDE_6},
        ]

        # Add betting buttons
        for side in self.sides:
            btn = discord.ui.Button(
                style=discord.ButtonStyle.secondary,
                emoji=side['emoji'],
                custom_id=side['id'],
                row=0 if self.sides.index(side) < 3 else 1
            )
            btn.callback = self.create_callback(side)
            self.add_item(btn)

        # Control buttons
        self.spin_btn = discord.ui.Button(
            label="QUAY NGAY!", 
            style=discord.ButtonStyle.success,
            emoji="🎲",
            row=2,
            custom_id="spin_now"
        )
        self.spin_btn.callback = self.spin_callback
        self.add_item(self.spin_btn)

    def create_callback(self, side):
        async def callback(interaction: discord.Interaction):
            # Check current balance
            points = await self.db.get_player_points(interaction.user.id, interaction.guild_id)
            locked = self.locked_balance.get(interaction.user.id, 0)
            available = points - locked
            
            modal = BetModal(
                side_name=side['name'], 
                side_emoji=side['emoji'],
                max_bet=500000,
                current_balance=available, # Pass available balance for UI hint
                callback_func=self.process_bet
            )
            await interaction.response.send_modal(modal)
        return callback

    async def process_bet(self, interaction: discord.Interaction, amount, side_name, side_emoji):
        user_id = interaction.user.id
        
        # Re-verify funds with lock
        points = await self.db.get_player_points(interaction.user.id, interaction.guild_id)
        locked = self.locked_balance.get(user_id, 0)
        
        if (locked + amount) > points:
            await interaction.response.send_message(f"❌ Bạn không đủ tiền! (Đã cược: {locked:,}, muốn cược thêm: {amount:,})", ephemeral=True)
            return

        # Lock funds (don't deduct from DB yet)
        self.locked_balance[user_id] = locked + amount
        new_locked = self.locked_balance[user_id]
        
        if user_id not in self.bets:
            self.bets[user_id] = {}
            self.user_total_bet[user_id] = 0
            
        current_side_bet = self.bets[user_id].get(side_name, 0)
        self.bets[user_id][side_name] = current_side_bet + amount
        self.user_total_bet[user_id] += amount
        
        remaining = points - new_locked
        
        await interaction.response.send_message(
            f"✅ Đã cược **{amount:,}** coinz {emojis.ANIMATED_EMOJI_COINZ} vào {side_emoji} {side_name}!\n"
            f"Số dư khả dụng: **{remaining:,}** coinz {emojis.ANIMATED_EMOJI_COINZ}", 
            ephemeral=True
        )
        # Note: We do NOT call update_embed here anymore to avoid rate-limit clashes with the animation loop.
        # The animation loop (running every 1s) will pick up the new bet state automatically.

    async def spin_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.host_id:
            await interaction.response.send_message("❌ Chỉ người tạo phòng mới được bấm quay!", ephemeral=True)
            return
        
        self.stop_event.set() # Stop animation
        await interaction.response.defer()
        self.stop() # Stop interactions

    async def update_embed(self, dice_animation_str=None):
        if not self.message: return
        try:
            embed = self.message.embeds[0]
            
            # 1. Update DICE ANIMATION field (Index 1) if provided
            if dice_animation_str:
                 embed.set_field_at(1, name="🎲 Xúc Xắc Đang Lắc...", value=dice_animation_str, inline=False)

            # 2. Update TOTAL BETS field (Index 0)
            total_pot = sum(self.user_total_bet.values())
            total_players = len(self.bets)
            embed.set_field_at(0, name="💰 Tổng Cược", value=f"**{total_pot:,}** coinz ({total_players} người chơi)", inline=False)
            
            # 3. Update BET LIST field (Index 2)
            bet_details = []
            for uid, user_bets in self.bets.items():
                b_str = []
                for s_name, amt in user_bets.items():
                    s_emoji = next((s['emoji'] for s in self.sides if s['name'] == s_name), "")
                    b_str.append(f"{s_emoji} {amt:,}")
                bet_details.append(f"<@{uid}>: " + " | ".join(b_str))
            
            val = "\n".join(bet_details) if bet_details else "Chưa có cược"
            if len(val) > 1024: val = val[:1000] + "..."
            
            if len(embed.fields) > 2:
                embed.set_field_at(2, name="📝 Danh sách cược", value=val, inline=False)
            else:
                embed.add_field(name="📝 Danh sách cược", value=val, inline=False)

            await self.message.edit(embed=embed, view=self)
        except discord.NotFound:
            pass
        except Exception as e:
            print(f"Error updating embed: {e}")

class BauCuaCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db: DatabaseManager):
        self.bot = bot
        self.db = db
        self.sides_map = {
            "Alien": emojis.SIDE_1,
            "Star": emojis.SIDE_2,
            "Rocket": emojis.SIDE_3,
            "Planet": emojis.SIDE_4,
            "Galaxy": emojis.SIDE_5,
            "Comet": emojis.SIDE_6
        }
        self.sides_list = list(self.sides_map.keys())
        self.emoji_list = [emojis.SIDE_1, emojis.SIDE_2, emojis.SIDE_3, emojis.SIDE_4, emojis.SIDE_5, emojis.SIDE_6]

    async def animate_waiting(self, view: BauCuaView):
        """Animates the dice in the lobby while waiting"""
        # Pos 0, 2, 4: 1->6
        # Pos 1, 3, 5: 3->6->1->2 (Started from index 2)
        idx1 = 0
        idx2 = 2
        
        while not view.stop_event.is_set():
            if view.message:
                try:
                    # Calc current emojis
                    current_emojis = []
                    for i in range(6):
                        if i % 2 == 0: # 0, 2, 4
                             emoji = self.emoji_list[idx1] 
                        else: # 1, 3, 5
                             emoji = self.emoji_list[idx2]
                        current_emojis.append(emoji)
                    
                    # Update indices
                    idx1 = (idx1 + 1) % 6
                    idx2 = (idx2 + 1) % 6
                    
                    # Format string
                    display_str = f"{current_emojis[0]} {current_emojis[1]} {current_emojis[2]}\n{current_emojis[3]} {current_emojis[4]} {current_emojis[5]}"
                    
                    # Call single update method for everything
                    await view.update_embed(dice_animation_str=display_str)

                except Exception as e:
                    print(f"Animation error: {e}")
            
            # Wait 1.0s - The absolute fastest compliant SUSTAINED speed
            # Since we merged updates, this won't clash with betting updates
            await asyncio.sleep(1.0)

    async def start_game(self, interaction: discord.Interaction):
        # Initial Embed
        embed = discord.Embed(
            title="🎲 BẦU CUA TÔM CÁ (Space Edition) 🎲",
            description=(
                f"Hãy đặt cược vào các cửa bên dưới!\n"
                f"Tối đa cược: **500,000** coinz/lần\n"
                f"Người tạo phòng: {interaction.user.mention}\n"
                f"⚠️ Tiền sẽ được trừ và cộng sau khi quay xong!"
            ),
            color=config.COLOR_INFO
        )
        
        # Pre-add "Total Bet" field at index 0
        embed.add_field(name="💰 Tổng Cược", value="**0** coinz (0 người chơi)", inline=False)
        
        # Pre-add "Animation" field at index 1
        embed.add_field(name="🎲 Xúc Xắc Đang Lắc...", value=f"{emojis.SIDE_1} {emojis.SIDE_2} {emojis.SIDE_3}\n{emojis.SIDE_4} {emojis.SIDE_5} {emojis.SIDE_6}", inline=False)
        
        # Add "Bet List" field placeholder at index 2
        embed.add_field(name="� Danh sách cược", value="Chưa có cược", inline=False)

        view = BauCuaView(self.bot, self.db, interaction.user.id, timeout=120)
        
        await interaction.response.send_message(embed=embed, view=view)
        view.message = await interaction.original_response()
        
        # Start animation task
        anim_task = asyncio.create_task(self.animate_waiting(view))
        
        # Wait for timeout or manual stop
        await view.wait()
        
        # Ensure animation stops
        view.stop_event.set()
        await asyncio.sleep(0.5) # Allow task to finish logic
        anim_task.cancel()

        # Deduct Money First (Validation Phase)
        # We need to check if they STILL have money (since we didn't lock it in DB)
        # If they don't, we invalidate the bet.
        
        valid_bets = {} # {uid: {side: valid_amount}}
        
        current_balances = {} # cache to avoid spamming DB
        
        for uid, user_bets in view.bets.items():
            total_bet_req = sum(user_bets.values())
            
            # Get fresh balance
            if uid not in current_balances:
                current_balances[uid] = await self.db.get_player_points(uid, interaction.guild_id)
            
            balance = current_balances[uid]
            
            if balance >= total_bet_req:
                # Valid
                valid_bets[uid] = user_bets
                # Deduct now
                await self.db.add_points(uid, interaction.guild_id, -total_bet_req)
                current_balances[uid] -= total_bet_req
            else:
                # Not enough funds anymore!
                user = self.bot.get_user(uid)
                name = user.name if user else uid
                try:
                     await interaction.channel.send(f"⚠️ <@{uid}> không đủ tiền để thực hiện cược (Cần: {total_bet_req}, Có: {balance}). Hủy cược!")
                except: pass
        
        # Determine Results
        
        # Animation: 3 Loading -> Reveal
        load_embed = discord.Embed(
            title="🎲 ĐANG QUAY...",
            description="",
            color=config.COLOR_WARNING
        )
        
        # Helper to format reveal
        def format_reveal(revealed_indices, results):
            # 3 slots.
            slots = []
            for i in range(3):
                if i in revealed_indices:
                    slots.append(self.sides_map[results[i]])
                else:
                    slots.append(emojis.LOADING)
            return " | ".join(slots)

        result_names = [random.choice(self.sides_list) for _ in range(3)]
        
        # Step 0: All Loading
        load_embed.description = f"# {emojis.LOADING} | {emojis.LOADING} | {emojis.LOADING}"
        await view.message.edit(embed=load_embed, view=None)
        await asyncio.sleep(1.5)
        
        # Step 1: Reveal 1
        load_embed.description = f"# {format_reveal([0], result_names)}"
        await view.message.edit(embed=load_embed)
        await asyncio.sleep(1.5)
        
        # Step 2: Reveal 2
        load_embed.description = f"# {format_reveal([0, 1], result_names)}"
        await view.message.edit(embed=load_embed)
        await asyncio.sleep(1.5)
         
        # Step 3: Reveal 3 (Final)
        final_desc = f"# {format_reveal([0, 1, 2], result_names)}"
        load_embed.description = final_desc
        await view.message.edit(embed=load_embed)
        await asyncio.sleep(1)

        
        # Calculate Winnings & Summary
        summary_lines = []
        
        for user_id, user_bets in valid_bets.items():
            total_bet = sum(user_bets.values())
            total_payout = 0
            win_details = []
            
            for side_name, amount in user_bets.items():
                count = result_names.count(side_name)
                if count > 0:
                    profit = amount * count
                    # Payout = Bet + Profit
                    payout_for_side = amount + profit
                    total_payout += payout_for_side
                    
                    side_emoji = self.sides_map[side_name]
                    # Format: 🐟 x2 (+Bonus)
                    win_details.append(f"{side_emoji} x{count} (+{profit:,})")

            # Update DB if payout > 0
            if total_payout > 0:
                await self.db.add_points(user_id, interaction.guild_id, total_payout)

            net_outcome = total_payout - total_bet
            user_mention = f"<@{user_id}>"
            
            if net_outcome > 0:
                # Winner
                detail_str = ", ".join(win_details)
                line = f"🎉 {user_mention}: **+{net_outcome:,}** {emojis.ANIMATED_EMOJI_COINZ}\n   ╚ {detail_str}"
                summary_lines.append(line)
            elif net_outcome == 0:
                # Break even
                line = f"😐 {user_mention}: **Hòa vốn** {emojis.ANIMATED_EMOJI_COINZ}"
                summary_lines.append(line)
            else:
                # Loser
                # Show negative amount
                line = f"💸 {user_mention}: **{net_outcome:,}** {emojis.ANIMATED_EMOJI_COINZ}"
                summary_lines.append(line)

        # Final Result Embed
        result_emojis = [self.sides_map[name] for name in result_names]
        result_str = " ".join(result_emojis)
        end_embed = discord.Embed(
            title=f"🎲 KẾT QUẢ: {result_str}",
            color=config.COLOR_SUCCESS
        )
        end_embed.description = final_desc + "\n\n"
        
        if summary_lines:
            end_embed.add_field(name="📊 Tổng Kết", value="\n".join(summary_lines), inline=False)
        else:
            end_embed.add_field(name="😅 Kết Quả", value="Không có người chơi nào đặt cược!", inline=False)
            
        await view.message.edit(embed=end_embed)

    async def stop_game(self, interaction: discord.Interaction):
        await interaction.response.send_message("⚠️ Game Bầu Cua tự động kết thúc sau khi quay. Hãy bấm nút 'QUAY NGAY'!", ephemeral=True)

async def setup(bot: commands.Bot):
    db = DatabaseManager(config.DATABASE_PATH)
    await bot.add_cog(BauCuaCog(bot, db))
