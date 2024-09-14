from django.contrib.auth.models import User, auth
from django.contrib import messages
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Profile, Post, LikePost, FollowerCount
from .serializers import *
from itertools import chain
import random
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
class GenerateTaskView(APIView):
    def post(self, request):
        # Get inputs from the request data
        '''
        location = request.data.get("location")
        time_limit = request.data.get("time_limit")
        budget = request.data.get("budget")
        transportation = request.data.get("transportation")

        if not all([location, time_limit, budget, transportation]):
            return Response({"error": "All fields are required."}, status=400)
            '''

        # Set up the chat session as you did in task.py
        generation_config = {
            "temperature": 1.5,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        chat_session = model.start_chat(    
            history=[
                {
                "role": "user",
                "parts": [
                    "i am participating creating an app. this is my idea:\nAI-Powered \"Microadventure\" Generator. It will be called SideQuest.\n\nChallenge: Build a tool that helps people inject tiny, spontaneous adventures into their ordinary life, tailored to their location and time constraints.\nHow it works:\nLeverages hyper-local data, analyzes the user's schedule for pockets of free time, and considers their interests.\nIt's NOT just generic suggestions, but might say: \"You have 20 mins before your next meeting. Walk two blocks in the opposite direction of your usual path, find something blue, take a photo.\"\nThe goal is to break up routines, foster attentiveness to one's surroundings, and add a sense of the unexpected to everyday life. \n\nThe goal is once a day when you open the app, you are prompted to start a sidequest. When you click to start it asks you a series of questions, such as how much time you have (up to 30 minutes) and what modes of transportation you have available. Subsequently it will access your location using a google maps API (or something similar) and find all landmarks or things to do. It will calculate whether you can complete this task by making sure you can complete the task in your given time limit given your mode of transportation.  You do the task, take a picture of you doing it, and upload for your friends to see where they can comment on and enjoy seeing your sidequests. \n\nfor example say you are next to the CN Tower, and you say you have 15 minutes. a particular task may be \"go feed the ducks at bobbiee rosenfeld park\" (which is a 3 minute walk away. Given this information, generate a series of possible tasks someone may do with 30 minutes of time, walking, in the heart of downtown Toronto. for a promp like that id want a task like one of the following: Street Art Exploration:\n\n    Task: Walk to Graffiti Alley and find a mural that features an animal. Take a photo and share your thoughts on the artwork.\n    Location: Graffiti Alley (about 10 minutes from CN Tower)\n\nHidden Green Spaces:\n\n    Task: Walk to St. Andrew's Playground Park, find a bench, and spend 5 minutes observing the surroundings. Take a picture of something interesting you notice.\n    Location: St. Andrew's Playground Park (about 12 minutes from CN Tower)\n\nArchitectural Discovery:\n\n    Task: Head to the Gooderham Building (also known as the Flatiron Building). Take a photo of the building and research one interesting fact about its history to share.\n    Location: Gooderham Building (about 15 minutes from CN Tower)\n\nPublic Art Scavenger Hunt:\n\n    Task: Walk to the \"Toronto Sign\" at Nathan Phillips Square. Take a photo of yourself with the sign and look for a nearby piece of public art to photograph.\n    Location: Nathan Phillips Square (about 18 minutes from CN Tower)\n\nCultural Immersion:\n\n    Task: Visit the Art Gallery of Ontario's outdoor sculptures. Choose one sculpture, take a photo, and write a brief description of what you think it represents.\n    Location: Art Gallery of Ontario (about 20 minutes from CN Tower)\n\nNature Walk:\n\n    Task: Walk to the Toronto Music Garden, find a spot to sit, and spend 5 minutes listening to the sounds around you. Take a picture of your favorite spot in the garden.\n    Location: Toronto Music Garden (about 15 minutes from CN Tower)\n\nHistorical Exploration:\n\n    Task: Head to the Royal Alexandra Theatre, take a photo of the building, and find out one interesting fact about its history to share.\n    Location: Royal Alexandra Theatre (about 10 minutes from CN Tower)\n\nCulinary Adventure:\n\n    Task: Walk to St. Lawrence Market, buy a snack from a vendor you haven't tried before, and take a photo of your treat. Share your experience with the taste and atmosphere.\n    Location: St. Lawrence Market (about 20 minutes from CN Tower)\n\nMindfulness Moment:\n\n    Task: Walk to Simcoe Park, find a quiet spot, and spend 5 minutes practicing mindfulness or meditation. Take a picture of your surroundings and describe how it made you feel.\n    Location: Simcoe Park (about 5 minutes from CN Tower)\n\nHistorical Monument:\n\n    Task: Visit the monument of John Simcoe, take a photo, and share a brief description of who he was and why he is significant to Toronto.\n    Location: Simcoe Park (about 5 minutes from CN Tower) Urban Fitness Challenge:\n\n    Task: Jog along the Toronto Waterfront Trail from Harbourfront Centre to Sugar Beach. Take a photo of the view of Lake Ontario from Sugar Beach.\n    Location: Harbourfront Centre to Sugar Beach (about 25 minutes from CN Tower)\n\nStairway Adventure:\n\n    Task: Climb to the top of Casa Loma's Baldwin Steps. Take a photo from the top overlooking the city skyline and share a fun fact about the steps' history.\n    Location: Casa Loma Baldwin Steps (about 25 minutes from CN Tower)\n\nBike Ride Exploration:\n\n    Task: Rent a bike at the Bike Share Toronto station near Union Station. Cycle along the Martin Goodman Trail to Humber Bay Arch Bridge. Take a photo of the bridge and share your favorite part of the ride.\n    Location: Martin Goodman Trail to Humber Bay Arch Bridge (about 30 minutes from CN Tower)\n\nKayaking Adventure:\n\n    Task: Rent a kayak at Harbourfront Canoe & Kayak Centre. Paddle around Toronto Islands and take a photo of the skyline from the water.\n    Location: Harbourfront Canoe & Kayak Centre (about 20 minutes from CN Tower)\n\nYoga in the Park:\n\n    Task: Head to Trinity Bellwoods Park. Find a quiet spot, practice a yoga pose, and take a photo or video. Reflect on how being outdoors enhances your yoga experience.\n    Location: Trinity Bellwoods Park (about 20 minutes from CN Tower) learn from them, these are all interesting and fun tasks. I want tasks like these. For further learning, look at the following list of tasks from different cities, budgets, environments, amounts of time, and available transportation methods: Tokyo, Japan\n\n    Shibuya Crossing Experience:\n        Transport: Walking\n        Budget: Free\n        Task: Walk across the famous Shibuya Crossing. Take a photo from the Starbucks overlooking the intersection.\n        Location: Shibuya\n\n    Tsukiji Outer Market Food Tour:\n        Transport: Subway/Walking\n        Budget: $20-$30\n        Task: Visit Tsukiji Outer Market. Sample sushi and other street foods. Take photos of your favorite dishes.\n        Location: Tsukiji\n\nParis, France\n\n    Eiffel Tower Picnic:\n        Transport: Walking/Subway\n        Budget: $10-$20\n        Task: Have a picnic at Champ de Mars with a view of the Eiffel Tower. Take photos of your picnic setup.\n        Location: Champ de Mars\n\n    Louvre Museum Exploration:\n        Transport: Subway\n        Budget: $15-$20 (entry fee)\n        Task: Visit the Louvre Museum. Take photos of the Mona Lisa and other famous artworks.\n        Location: Louvre Museum\n\nNew York City, USA\n\n    Central Park Bike Ride:\n        Transport: Bike\n        Budget: $10 (bike rental)\n        Task: Rent a bike and ride through Central Park. Take photos of iconic landmarks like Bow Bridge.\n        Location: Central Park\n\n    Times Square Night Walk:\n        Transport: Walking\n        Budget: Free\n        Task: Walk through Times Square at night. Take photos of the bright lights and bustling crowds.\n        Location: Times Square\n\nSuburbs\nCupertino, California, USA\n\n    Apple Park Visitor Center:\n        Transport: Car\n        Budget: Free\n        Task: Visit the Apple Park Visitor Center. Take photos of the building and Apple merchandise.\n        Location: Cupertino\n\n    Ranch 99 Market Tour:\n        Transport: Car\n        Budget: $10-$20\n        Task: Explore Ranch 99 Market. Buy and sample exotic fruits and snacks. Take photos of your finds.\n        Location: Cupertino\n\nRichmond, British Columbia, Canada\n\n    Steveston Village Walk:\n        Transport: Car/Walking\n        Budget: Free\n        Task: Walk around Steveston Village. Take photos of the historic fishing village and waterfront.\n        Location: Steveston Village\n\n    Aberdeen Centre Food Court:\n        Transport: Car\n        Budget: $10-$20\n        Task: Visit Aberdeen Centre. Sample various foods from the food court and take photos of your meals.\n        Location: Richmond\n\nBeaches\nBondi Beach, Sydney, Australia\n\n    Bondi to Coogee Walk:\n        Transport: Walking\n        Budget: Free\n        Task: Walk the coastal path from Bondi to Coogee. Take photos of the scenic views and beaches.\n        Location: Bondi Beach\n\n    Surf Lesson at Bondi:\n        Transport: Walking\n        Budget: $50-$100 (lesson fee)\n        Task: Take a surf lesson at Bondi Beach. Take photos of yourself riding the waves.\n        Location: Bondi Beach\n\nWaikiki Beach, Honolulu, Hawaii, USA\n\n    Sunset at Waikiki:\n        Transport: Walking\n        Budget: Free\n        Task: Watch the sunset at Waikiki Beach. Take photos of the changing colors over the ocean.\n        Location: Waikiki Beach\n\n    Snorkeling at Hanauma Bay:\n        Transport: Car/Bus\n        Budget: $20-$30 (entry fee + gear rental)\n        Task: Snorkel at Hanauma Bay. Take underwater photos of the vibrant marine life.\n        Location: Hanauma Bay\n\nRural Areas\nTaos, New Mexico, USA\n\n    Taos Pueblo Visit:\n        Transport: Car\n        Budget: $10-$20 (entry fee)\n        Task: Visit Taos Pueblo. Take photos of the ancient dwellings and learn about the history.\n        Location: Taos Pueblo\n\n    Hot Air Balloon Ride:\n        Transport: Car\n        Budget: $200-$300\n        Task: Take a hot air balloon ride over Taos. Capture panoramic photos of the landscape.\n        Location: Taos\n\nInverness, Scotland\n\n    Loch Ness Monster Hunt:\n        Transport: Car\n        Budget: Free\n        Task: Visit Loch Ness and search for the Loch Ness Monster. Take photos of the lake and surrounding scenery.\n        Location: Loch Ness\n\n    Inverness Castle Tour:\n        Transport: Walking\n        Budget: $10-$20\n        Task: Tour Inverness Castle. Take photos of the historic site and the view from the castle.\n        Location: Inverness\n\nForests\nBanff National Park, Alberta, Canada\n\n    Johnston Canyon Hike:\n        Transport: Car/Hiking\n        Budget: Free\n        Task: Hike through Johnston Canyon to the Upper Falls. Take photos of the waterfalls and canyon.\n        Location: Banff National Park\n\n    Lake Louise Canoeing:\n        Transport: Car/Canoe\n        Budget: $30-$40 (canoe rental)\n        Task: Canoe on Lake Louise. Take photos of the turquoise water and surrounding mountains.\n        Location: Lake Louise\n\nBlack Forest, Germany\n\n    Triberg Waterfalls Visit:\n        Transport: Car\n        Budget: $5-$10 (entry fee)\n        Task: Visit the Triberg Waterfalls. Take photos of the waterfalls and the lush forest.\n        Location: Black Forest\n\n    Black Forest Cake Tasting:\n        Transport: Car\n        Budget: $10-$20\n        Task: Visit a local bakery in the Black Forest. Taste authentic Black Forest cake and take photos of the dessert.\n        Location: Black Forest\n\nDesert\nSedona, Arizona, USA\n\n    Red Rock State Park Hike:\n        Transport: Car/Hiking\n        Budget: $10-$20 (entry fee)\n        Task: Hike in Red Rock State Park. Take photos of the red rock formations and desert landscape.\n        Location: Sedona\n\n    Sedona Vortex Tour:\n        Transport: Car\n        Budget: $30-$40\n        Task: Take a guided tour to one of Sedona's vortex sites. Take photos of the scenic views and learn about the vortex energy.\n        Location: Sedona\n\nMarrakech, Morocco\n\n    Jemaa el-Fnaa Market:\n        Transport: Walking\n        Budget: $10-$20\n        Task: Explore the bustling Jemaa el-Fnaa market. Take photos of the vibrant stalls and try local street food.\n        Location: Marrakech\n\n    Desert Camel Ride:\n        Transport: Car/Camel\n        Budget: $50-$100\n        Task: Take a camel ride in the Agafay Desert near Marrakech. Take photos of the desert landscape and your camel ride experience.\n        Location: Agafay Desert\n\nCoastal Towns\nAmalfi Coast, Italy\n\n    Positano Beach Day:\n        Transport: Car\n        Budget: Free\n        Task: Spend a day at the beach in Positano. Take photos of the colorful buildings and clear blue water.\n        Location: Positano\n\n    Ravello Gardens Tour:\n        Transport: Car\n        Budget: $10-$20 (entry fee)\n        Task: Visit the gardens at Villa Rufolo in Ravello. Take photos of the beautiful gardens and coastal views.\n        Location: Ravello\n\nCape Cod, Massachusetts, USA\n\n    Whale Watching Tour:\n        Transport: Car/Boat\n        Budget: $50-$100\n        Task: Take a whale watching tour off the coast of Cape Cod. Take photos of the whales and other marine life.\n        Location: Cape Cod\n\n    Provincetown Art Walk:\n        Transport: Car/Walking\n        Budget: Free\n        Task: Walk through Provincetown and explore the local art galleries. Take photos of your favorite artworks and street scenes.\n        Location: Provincetown Again, please learn from these tasks as they encapsulate exactly what we are looking for in these tasks. From now on, I will feed you information and always generate me one random, interesting, yet unique task",
                ],
                },
                {
                "role": "model",
                "parts": [
                    "Okay, I'm ready to generate some exciting micro-adventures! Let's start with some information to get the ball rolling.\n\n**Please tell me:**\n\n* **Location:** Where in downtown Toronto are you starting from? (Near the CN Tower is good!) \n* **Time limit:**  How much time do you have (up to 30 minutes)?\n* **Transportation:** How will you be getting around (walking, transit, biking, etc.)? \n* **Any interests:** Are there any specific things you're into right now, like art, history, food, nature, etc.? \n\nOnce I have this info, I'll craft you a unique and engaging SideQuest! \n",
                ],
                },
            ]
        )

        location = "Waterloo"
        time_limit = "30 minutes"
        budget = 0
        transportation = "walk"


        response = chat_session.send_message(
            f"Location: {location}, Time Limit: {time_limit} minutes, Budget: {budget}, Transportation: {transportation}. Please also get rid of the why it fits section"
        )

        #work on storing tasks in a database
        return Response({"task": response.text})
        

# Signup View (User Registration)
class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if password != password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already taken'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user_login = authenticate(username=username, password=password)
        if user_login is not None:
            login(request, user_login)
            # Create profile for new user
            Profile.objects.create(user=user, id_user=user.id)
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'User creation failed'}, status=status.HTTP_400_BAD_REQUEST)


# Signin View (User Login)
class SigninView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Logout View
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        auth.logout(request)
        return Response(status=status.HTTP_200_OK)


# Profile Detail View (Retrieve and Update Profile)
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs.get('username'))


# Post List/Create View (Upload Post)
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.username)


# Like/Unlike Post View
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.user.username
        post_id = request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

        if like_filter is None:
            LikePost.objects.create(post_id=post_id, username=username)
            post.num_of_likes += 1
            post.save()
            return Response({'message': 'Liked successfully'}, status=status.HTTP_200_OK)
        else:
            like_filter.delete()
            post.num_of_likes -= 1
            post.save()
            return Response({'message': 'Unliked successfully'}, status=status.HTTP_200_OK)


# Follow/Unfollow View
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        follower = request.user.username
        user = request.data.get('user')

        if FollowerCount.objects.filter(follower=follower, user=user).exists():
            FollowerCount.objects.filter(follower=follower, user=user).delete()
            return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
        else:
            FollowerCount.objects.create(follower=follower, user=user)
            return Response({'message': 'Followed successfully'}, status=status.HTTP_200_OK)


# Search View
class SearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        users = User.objects.filter(username__icontains=username)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Index View (Feed and User Suggestions)
class IndexView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_following = FollowerCount.objects.filter(follower=request.user.username)
        user_following_list = [users.user for users in user_following]

        feed = [Post.objects.filter(user=usernames) for usernames in user_following_list]
        feed_list = list(chain(*feed))

        all_users = User.objects.all()
        user_following_all = [User.objects.get(username=user.user) for user in user_following]
        new_suggestion_list = [x for x in list(all_users) if x not in user_following_all]
        final_suggestion_list = [x for x in list(new_suggestion_list) if x != request.user]

        random.shuffle(final_suggestion_list)
        username_profile_list = [Profile.objects.filter(id_user=users.id) for users in final_suggestion_list]
        suggestions_username_profile_list = list(chain(*username_profile_list))[:4]

        serializer = PostSerializer(feed_list, many=True)
        suggestions_serializer = ProfileSerializer(suggestions_username_profile_list, many=True)

        return Response({
            'feed': serializer.data,
            'suggestions': suggestions_serializer.data
        })


# Settings View (Update Profile)
class SettingsView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# Terms View
class TermsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Return a simple response or HTML page content as needed
        return Response("Terms and Conditions")


# Profile View (View User Profile)
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            user_object = User.objects.get(username=pk)
            user_profile = Profile.objects.get(user=user_object)
            user_posts = Post.objects.filter(user=pk)
            user_post_length = user_posts.count()

            follower = request.user.username
            user = pk

            button_text = 'Unfollow' if FollowerCount.objects.filter(follower=follower, user=user).exists() else 'Follow'
            follower_count = FollowerCount.objects.filter(user=pk).count()
            following_count = FollowerCount.objects.filter(follower=pk).count()

            context = {
                'user_object': user_object,
                'user_profile': user_profile,
                'user_posts': user_posts,
                'user_post_length': user_post_length,
                'button_text': button_text,
                'follower_count': follower_count,
                'following_count': following_count
            }

            return Response(context)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response({'error': 'No posts found'}, status=status.HTTP_404_NOT_FOUND)
