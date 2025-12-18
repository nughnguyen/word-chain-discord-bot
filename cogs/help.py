import discord
from discord.ext import commands
from discord import app_commands
import platform
import datetime
from utils import emojis
from utils.views import DonationView
import config

class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.bot = bot
        
        # Link Buttons
        self.add_item(discord.ui.Button(
            label="Website", 
            style=discord.ButtonStyle.link, 
            url="https://quochung.id.vn", 
            emoji=emojis.EMOJI_LINK
        ))
        self.add_item(discord.ui.Button(
            label="Support Server", 
            style=discord.ButtonStyle.link, 
            url="https://dsc.gg/thenoicez", 
            emoji=emojis.EMOJI_DISCORD
        ))
        self.add_item(discord.ui.Button(
            label="Invite", 
            style=discord.ButtonStyle.link, 
            url="https://discord.com/oauth2/authorize?client_id=1305035261897343026&permissions=8&integration_type=0&scope=bot", 
            emoji=emojis.EMOJI_INVITE # Facebook or generic website emoji
        ))

    @discord.ui.select(
        placeholder="Marble Soda Menu",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Trang Chủ", description="Quay lại menu chính", emoji="🏠"),
            discord.SelectOption(label="Hướng Dẫn Tân Thủ", description="Cách chơi & Kiếm Coiz", emoji="📘"),
            discord.SelectOption(label="Câu Cá (Fishing)", description="Hệ thống câu cá RPG", emoji="🎣"),
            discord.SelectOption(label="Games Commands", description="Word Chain, Vua Tiếng Việt, Bầu Cua", emoji="🎮"),
            discord.SelectOption(label="Leaderboard Commands", description="Xem rank", emoji="🏆"),
            discord.SelectOption(label="Admin Commands", description="Admin tools", emoji="🛡️"),
            discord.SelectOption(label="Utility Commands", description="Bot info & others", emoji="🛠️"),
            discord.SelectOption(label="Donation", description="Support the bot", emoji=emojis.EMOJI_MOMO_PAY),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]
        
        embed = discord.Embed(
            title=f"{choice}",
            color=config.COLOR_INFO,
            timestamp=datetime.datetime.now()
        )
        
        if choice == "Trang Chủ":
            embed.title = "✨ CHÀO MỪNG ĐẾN VỚI MARBLE SODA BOT ✨"
            embed.description = (
                "**Marble Soda** là Bot giải trí đa năng số 1 Việt Nam! 🇻🇳\n"
                "Tham gia ngay vào thế giới minigame sôi động, hệ thống kinh tế độc đáo và các giải đấu hấp dẫn.\n\n"
                "🤖 **GIỚI THIỆU CHUNG:**\n"
                "> Bot cung cấp hệ thống **Câu Cá RPG** cày cuốc, các minigame trí tuệ như **Nối Từ, Vua Tiếng Việt** và các trò chơi may mắn như **Bầu Cua**.\n"
                "\n"
                "📜 **DANH MỤC MENU DƯỚI ĐÂY:**\n"
                "📘 **Hướng Dẫn Tân Thủ**: Cách kiếm Coiz và luật chơi cơ bản.\n"
                "🎣 **Câu Cá (Fishing)**: Hệ thống RPG, nâng cấp cần, săn Boss.\n"
                "🎮 **Games Commands**: Lệnh chơi Nối Từ, Bầu Cua, VTV.\n"
                "🏆 **Leaderboard**: Xem Top đại gia và cao thủ server.\n"
                "💎 **Donation**: Nạp ủng hộ Bot & Nhận quyền lợi VIP."
            )
            embed.color = 0x2b2d31
            
            # Main Commands Highlights
            embed.add_field(
                name="🚀 **LỆNH HỆ THỐNG & CÀI ĐẶT**",
                value=(
                    f"`/help` - Hiển thị Menu hướng dẫn tổng hợp\n"
                    f"`/donation` - Hệ thống nạp Coiz & Quyền lợi VIP\n"
                    f"`/set-game-channel` - Cài đặt kênh Minigame (Admin)\n"
                    f"`/kenh-cau-ca` - Cài đặt kênh Câu cá (Admin)\n"
                    f"`/stats` - Xem hồ sơ cá nhân"
                ),
                inline=False
            )

            # Bot Status
            ping = round(self.bot.latency * 1000)
            server_count = len(self.bot.guilds)
            user_count = sum(guild.member_count for guild in self.bot.guilds)
            
            status_text = (
                f"📡 Ping: `{ping}ms`\n"
                f"🏠 Servers: `{server_count}`\n"
                f"👥 Users: `{user_count:,}`\n"
                f"💻 Prefix: `{config.COMMAND_PREFIX}`"
            )
            
            embed.add_field(
                name="📊 **TRẠNG THÁI HỆ THỐNG**",
                value=status_text,
                inline=False
            )
            
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")

        elif choice == "Hướng Dẫn Tân Thủ":
            embed.description = "Chào mừng bạn đến với **Marble Soda**! Dưới đây là hướng dẫn cơ bản:"
            
            embed.add_field(
                name="🎮 **Cách Bắt Đầu**",
                value=(
                    "1. **Tìm Kênh Game**: Bot chỉ hoạt động ở các kênh được cấu hình.\n"
                    "   (Nếu chưa có, nhờ Admin dùng lệnh `/set-game-channel`)\n"
                    "2. **Bắt Đầu**: Gõ `/start` tại kênh game tương ứng (Nối Từ, Bầu Cua...)\n"
                    "3. **Kết Thúc**: Gõ `/stop` để dừng game và nhận thưởng."
                ),
                inline=False
            )
            
            embed.add_field(
                name=f"💰 **Bí Kíp Kiếm Coiz {emojis.ANIMATED_EMOJI_COIZ}**",
                value=(
                    "Coiz là đơn vị tiền tệ chính để chơi game và đua top.\n\n"
                    f"**1. Chơi Nối Từ (Word Chain):**\n"
                    f"   • Trả lời đúng: **+10 coiz** {emojis.ANIMATED_EMOJI_COIZ}\n"
                    f"   • Bonus Tốc độ: **+20 ~ 100 coiz** {emojis.ANIMATED_EMOJI_COIZ} (Trả lời càng nhanh càng nhiều tiền)\n"
                    f"   • Bonus Từ dài/khó: Nhận thêm thưởng!\n\n"
                    f"**2. Vua Tiếng Việt:**\n"
                    f"   • Giải mã từ khóa thành công: **Hàng nghìn coiz** {emojis.ANIMATED_EMOJI_COIZ} (Tùy độ khó)\n\n"
                    f"**3. Bầu Cua Tôm Cá:**\n"
                    f"   • Thử vận may đặt cược để nhân đôi, nhân ba tài sản!\n\n"
                    f"**4. Donation:**\n"
                    f"   • Nạp coiz {emojis.ANIMATED_EMOJI_COIZ} qua `/donation` để nhận ưu đãi cực khủng."
                ),
                inline=False
            )
            embed.add_field(
                name="⚠️ **Lưu Ý**",
                value="• Spam, cheat sẽ bị reset coiz hoặc ban khỏi hệ thống.",
                inline=False
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")

        elif choice == "Câu Cá (Fishing)":
            embed.title = "🎣 HƯỚNG DẪN CÂU CÁ (FISHING RPG)"
            embed.description = (
                "Chào mừng bạn đến với hệ thống **Câu Cá RPG** đỉnh cao! 🌊\n"
                "Hãy trở thành **Vua Câu Cá** huyền thoại, sưu tập các loài cá quý hiếm và kiếm hàng tỷ Coiz!\n\n"
                "**🎮 BẮT ĐẦU NGAY:**\n"
                "> Gõ `/fish` tại kênh câu cá để thả câu.\n"
                "> Gõ `/shop` để mua trang bị hỗ trợ.\n"
                "> Gõ `/inventory` để xem chiến lợi phẩm."
            )
            
            embed.add_field(
                name="⚙️ **Cơ Chế Gameplay**",
                value=(
                    f"{emojis.ANIMATED_EMOJI_DOT} **Power (Sức Mạnh)**: Giúp câu được **Cá To (Size to)**, bán được nhiều tiền hơn.\n"
                    f"{emojis.ANIMATED_EMOJI_DOT} **Luck (May Mắn)**: Tăng tỷ lệ gặp **Cá Hiếm** (Legendary, Mythical...) và nhặt được **Kho Báu**.\n"
                    f"{emojis.ANIMATED_EMOJI_DOT} **Độ Bền**: Mỗi lần câu sẽ giảm độ bền của cần. Khi về 0, cần sẽ bị gãy! (Trừ Cần Nhựa/Donator)."
                ),
                inline=False
            )

            embed.add_field(
                name="🎒 **Trang Bị & Vật Phẩm**",
                value=(
                    f"🎣 **Cần Câu (Rods)**: Nâng cấp cần xịn để tăng mạnh Power & Luck. Cần càng đắt, độ bền càng cao.\n"
                    f"🪱 **Mồi Câu (Baits)**: Buff chỉ số tạm thời. Đặc biệt **Nam Châm** {emojis.BAIT_MAGNET} giúp hút 2-5 con cá cùng lúc!\n"
                    f"🧿 **Bùa Chú (Charms)**: Buff sức mạnh trong thời gian ngắn (có thể cộng dồn)."
                ),
                inline=False
            )

            embed.add_field(
                name="🔥 **Tính Năng Đặc Sắc**",
                value=(
                    f"🌍 **Biomes (Khu Vực)**: Mở khóa các vùng đất mới (Biển, Trời, Núi Lửa...) để săn cá độc quyền giá trị cao.\n"
                    f"👑 **Boss Fish**: Những loài cá Vua cực hiếm, xuất hiện ngẫu nhiên. Sưu tập đủ để nhận huy hiệu danh giá.\n"
                    f"🐉 **Ngọc Rồng**: Tìm đủ **7 Viên Ngọc Rồng** từ Kho Báu để triệu hồi Rồng Thần ban điều ước **Coiz**!"
                ),
                inline=False
            )
            
            embed.add_field(
                name="💎 **Phần Thưởng & Lợi Ích**",
                value=(
                    f"💰 **Kiếm Coiz**: Bán cá để làm giàu, đua Top Tỷ Phú.\n"
                    f"⭐ **Level Up**: Nhận XP từ mỗi lần câu để thăng cấp và mở khóa tính năng mới.\n"
                    f"🏆 **Thành Tựu**: Sưu tập các Huy Hiệu (Badges) để khẳng định đẳng cấp."
                ),
                inline=False
            )
            
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")

        elif choice == "Games Commands":
            embed.description = "Hướng dẫn chi tiết các trò chơi:"
            
            # Word Chain Info
            embed.add_field(
                name="🔤 **Nối Từ (Word Chain)**",
                value=(
                    f"• **Luật chơi**: Nối tiếp từ bắt đầu bằng chữ cái cuối của từ trước.\n"
                    f"• **Lệnh**:\n"
                    f"  `/start` - Bắt đầu game\n"
                    f"  `/stop` - Dừng game (Kết thúc & trao giải)\n"
                    f"  `/challenge-bot` - ⚔️ Thách đấu Bot (Solo)\n"
                    f"• **Hỗ trợ**:\n"
                    f"  `/hint` - Gợi ý nhận ký tự tiếp theo ({config.HINT_COST} Coiz {emojis.ANIMATED_EMOJI_COIZ})\n"
                    f"  `/pass` - Bỏ lượt an toàn ({config.PASS_COST} Coiz {emojis.ANIMATED_EMOJI_COIZ})\n"
                    f"• **Điểm Thưởng & Phạt**:\n"
                    f"  ✅ **Đúng**: +10 Coiz {emojis.ANIMATED_EMOJI_COIZ} (+Bonus Level/Từ dài)\n"
                    f"  ⚡ **Tốc độ**: <5s (+100), <10s (+50), <20s (+20)\n"
                    f"  ❌ **Sai**: -2 Coiz {emojis.ANIMATED_EMOJI_COIZ}/lần (Tối đa 5 lần/lượt)\n"
                    f"  🐌 **Timeout**: -10 Coiz {emojis.ANIMATED_EMOJI_COIZ} (Mất lượt)"
                ),
                inline=False
            )
            
            # Vua Tieng Viet Info
            embed.add_field(
                name="👑 **Vua Tiếng Việt**",
                value=(
                    f"• **Luật chơi**: Sắp xếp ký tự bị xáo trộn thành từ có nghĩa.\n"
                    f"• **Lệnh**:\n"
                    f"  `/start` - Bắt đầu game tại kênh VTV\n"
                    f"  `/stop` - Dừng game\n"
                    f"• **Cách chơi**: Gõ đáp án trực tiếp vào chat.\n"
                    f"• **Phần thưởng**: Từ {config.POINTS_VUA_TIENG_VIET:,} đến {config.POINTS_VUA_TIENG_VIET_SIEU_KHO:,} Coiz (Tùy độ khó)!"
                ),
                inline=False
            )

            # Bau Cua Info
            embed.add_field(
                name="🎲 **Bầu Cua Tôm Cá**",
                value=(
                    f"• **Luật chơi**: Đặt cược vào 6 cửa (Nai, Bầu, Mèo, Cá, Cua, Tôm).\n"
                    f"• **Lệnh**:\n"
                    f"  `/start` - Bắt đầu game tại kênh Bầu Cua\n"
                    f"• **Cách chơi**: Dùng các nút bấm để đặt cược (Không giới hạn số tiền).\n"
                    f"• **Tỷ lệ thắng**: x1, x2, x3 tùy số mặt xúc xắc xuất hiện."
                ),
                inline=False
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")

        elif choice == "Leaderboard Commands":
            embed.description = "Xem bảng xếp hạng người chơi:"
            embed.add_field(
                name="📊 **Thống Kê**",
                value=(
                    "`/leaderboard` - Xem Top Server\n"
                    "`/stats [user]` - Xem thông tin cá nhân (Rank, Coiz, WinRate...)"
                ),
                inline=False
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")            
        
        elif choice == "Admin Commands":
            embed.description = "Các lệnh quản lý (chỉ dành cho Admin):"
            embed.add_field(
                name="⚙️ **Cài Đặt Game**",
                value=(
                    "`/kenh-noi-tu-vn` - Set kênh Nối Từ (VN)\n"
                    "`/kenh-noi-tu-en` - Set kênh Nối Từ (EN)\n"
                    "`/kenh-vua-tieng-viet` - Set kênh VTV\n"
                    "`/kenh-bau-cua` - Set kênh Bầu Cua\n"
                    "`/set-game-channel` - Cài đặt nâng cao"
                ),
                inline=False
            )
            embed.add_field(
                name="💰 **Quản Lý Coiz/Stats**",
                value=(
                    f"`/add-coiz [user] [amount]` - Cộng coiz {emojis.ANIMATED_EMOJI_COIZ} (Chỉ dành cho Owner)\n"
                    f"`/subtract-coiz [user] [amount]` - Trừ coiz {emojis.ANIMATED_EMOJI_COIZ} (Chỉ dành cho Owner)\n"
                    f"`/chuyen-coiz [user] [amount]` - Chuyển coiz {emojis.ANIMATED_EMOJI_COIZ}\n"
                    f"`/reset-coiz [user]` - Set coiz {emojis.ANIMATED_EMOJI_COIZ} về 0 (Chỉ dành cho Owner)\n"
                    f"`/reset-stats [user]` - Reset toàn bộ chỉ số game (Chỉ dành cho Owner)"
                ),
                inline=False
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")            
      
        elif choice == "Utility Commands":
            embed.description = "Thông tin khác về Bot:"
            embed.add_field(
                name="ℹ️ **Thông Tin**",
                value=(
                    f"• **Developer**: Quốc Hưng\n"
                    f"• **Prefix**: `{config.COMMAND_PREFIX}`\n"
                    f"• **Version**: 2.2.0"
                ),
                inline=False
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")

        elif choice == "Donation":
            embed.title = "💎 NẠP COIZ | ỦNG HỘ SERVER"
            embed.description = (
                "Chào mừng bạn đến với hệ thống nạp Coiz tự động 24/7!\n\n"
                "**🎁 QUYỀN LỢI KHI NẠP COIZ:**\n"
                "✨ Tham gia các minigame giải trí\n"
                "✨ Đua Top Tỷ Phú Server\n"
                "✨ Mua các vật phẩm/quyền lợi (sắp ra mắt)\n"
                "❤️ Góp phần duy trì Bot hoạt động ổn định\n\n"
                "**💰 TỶ GIÁ QUY ĐỔI:**\n"
                f"💵 `1,000 VND` = `{config.COIZ_PER_1000VND:,} Coiz` {emojis.ANIMATED_EMOJI_COIZ}\n"
                f"🔥 **Khuyến mãi:** Tặng thêm 10% khi nạp trên 50k!\n"
                f"🎣 **Đặc biệt:** Nạp tối thiểu **10,000 VND** nhận ngay **Cần Nhà Tài Trợ** (Donator Rod)!\n\n"
                "**💳 PHƯƠNG THỨC THANH TOÁN:**\n"
                "1. **MOMO** - Ví điện tử thông dụng\n"
                "2. **VNPAY** - Quét mã tiện lợi\n"
                "3. **VIETQR** - Chuyển khoản mọi ngân hàng (MB, VCB, OCB...)\n\n"
                "👇 **Chọn phương thức thanh toán bên dưới để bắt đầu:**"
            )
            embed.color = config.COLOR_GOLD
            embed.set_footer(text="Hệ thống xử lý tự động trong 1-3 phút • Cảm ơn bạn đã ủng hộ!")
            embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")
            await interaction.response.edit_message(embed=embed, view=DonationView())
            return
            
        await interaction.response.edit_message(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Hiển thị menu hướng dẫn")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="✨ CHÀO MỪNG ĐẾN VỚI MARBLE SODA BOT ✨",
            description=(
                "**Marble Soda** là Bot giải trí đa năng số 1 Việt Nam! 🇻🇳\n"
                "Tham gia ngay vào thế giới minigame sôi động, hệ thống kinh tế độc đáo và các giải đấu hấp dẫn.\n\n"
                "🤖 **GIỚI THIỆU CHUNG:**\n"
                "> Bot cung cấp hệ thống **Câu Cá RPG** cày cuốc, các minigame trí tuệ như **Nối Từ, Vua Tiếng Việt** và các trò chơi may mắn như **Bầu Cua**.\n"
                "\n"
                "📜 **DANH MỤC MENU DƯỚI ĐÂY:**\n"
                "📘 **Hướng Dẫn Tân Thủ**: Cách kiếm Coiz và luật chơi cơ bản.\n"
                "🎣 **Câu Cá (Fishing)**: Hệ thống RPG, nâng cấp cần, săn Boss.\n"
                "🎮 **Games Commands**: Lệnh chơi Nối Từ, Bầu Cua, VTV.\n"
                "🏆 **Leaderboard**: Xem Top đại gia và cao thủ server.\n"
                "💎 **Donation**: Nạp ủng hộ Bot & Nhận quyền lợi VIP."
            ),
            color=0x2b2d31,
            timestamp=datetime.datetime.now()
        )
        
        # Main Commands Highlights
        embed.add_field(
            name="🚀 **LỆNH HỆ THỐNG & CÀI ĐẶT**",
            value=(
                f"`/help` - Hiển thị Menu hướng dẫn tổng hợp\n"
                f"`/donation` - Hệ thống nạp Coiz & Quyền lợi VIP\n"
                f"`/set-game-channel` - Cài đặt kênh Minigame (Admin)\n"
                f"`/kenh-cau-ca` - Cài đặt kênh Câu cá (Admin)\n"
                f"`/stats` - Xem hồ sơ cá nhân"
            ),
            inline=False
        )
        
        # Bot Status
        ping = round(self.bot.latency * 1000)
        server_count = len(self.bot.guilds)
        user_count = sum(guild.member_count for guild in self.bot.guilds)
        
        status_text = (
            f"📡 Ping: `{ping}ms`\n"
            f"🏠 Servers: `{server_count}`\n"
            f"👥 Users: `{user_count:,}`\n"
            f"💻 Prefix: `{config.COMMAND_PREFIX}`"
        )
        
        embed.add_field(
            name="📊 **TRẠNG THÁI HỆ THỐNG**",
            value=status_text,
            inline=False
        )
        
        # Image banner if available in config or user preference, otherwise skip or add empty field
        
        embed.set_image(url="https://cdn.discordapp.com/attachments/1305556786304127097/1327687391267389632/thenoicez.gif?ex=6940eafd&is=693f997d&hm=332f39b7a027ecfebdead2cd326f57c1502020fff8922b78c8fdb623fa49a43b&")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        view = HelpView(self.bot)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))
