import time
import math
import asyncio
from pyrogram.types import Message
from config import Config
import pyrogram

def timeFormatter(milliseconds: int) -> str:
	seconds, milliseconds = divmod(int(milliseconds),1000)
	minutes, seconds = divmod(seconds,60)
	hours, minutes = divmod(minutes,60)
	days,hours = divmod(hours,24)
	tmp = ((str(days) + "d, ") if days else "")+\
		((str(hours) + "h, ") if hours else "") + \
			((str(minutes) + "m, ") if minutes else "") + \
				((str(seconds) + "s, ") if seconds else "") + \
					((str(milliseconds) + "ms, ") if milliseconds else "")
	return tmp[:-2]

def humanbytes(size):
	# https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
	if not size:
		return ''
	power = 2**10
	n = 0
	power_dict = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
	while size > power:
		size /= power
		n+=1
	return str(round(size,2)) + " " + power_dict[n] + 'B'

async def progress_for_pyrogram(current: int, total: int, ud_type: str, message: Message, start):
	now = time.time()
	diff = now-start
	if round(diff%10.00) == 0 or current == total:
		percentage = current * 100/total
		speed = current/diff
		elapsed_time = round(diff) * 1000
		time_to_completion = round((total - current) / speed) * 1000
		estimated_total_time = elapsed_time + time_to_completion

		elapsed_time = timeFormatter(milliseconds = elapsed_time)
		estimated_total_time = timeFormatter(milliseconds=estimated_total_time)

		progress = '[{0}{1}]\n'.format(
			''.join(["●" for i in range(math.floor(percentage / 5))]),
			''.join(["○" for i in range(20 - math.floor(percentage / 5))])
		)
		tmp = progress + Config.PROGRESS.format(
			round(percentage, 2),
 			humanbytes(current),
			humanbytes(total),
			humanbytes(speed),
			estimated_total_time if estimated_total_time != '' else "0 s"
		)
		try:
			await message.edit(text=f'**{ud_type}**\n\n{tmp}',parse_mode='markdown')
			await asyncio.sleep(4)
		except:
			pass
		